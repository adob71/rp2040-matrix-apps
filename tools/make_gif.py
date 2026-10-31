"""Make README GIFs by running an app on your computer.

The apps only use three modules from the board: time, ws2812 and touch. Here
they are replaced by stand-ins with a fake clock that record every frame the
app shows, so the app's own code decides what the GIF contains.

Usage:
    python3 tools/make_gif.py emoji          # apps/emoji.py -> gifs/emoji.gif
    python3 tools/make_gif.py emoji dice     # several apps
    python3 tools/make_gif.py all            # every app listed in APPS below
"""
import random
import runpy
import sys
import types
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

# What to record for each app:
#   ms    how many milliseconds of app time to record (one loop of the animation)
#   taps  times (ms) at which a touch pad is "tapped", for apps that use touch
#   seed  random seed, for apps with random behaviour (change it to get another run)
#   glow  False draws plain round LEDs without the soft glow; the glow looks nicer but
#         makes GIFs with many frames 10-20x bigger, so it is off for those apps
APPS = {
    "avatar": dict(ms=10000),
    "count":  dict(ms=1000),
    "dice":   dict(ms=4000, taps=[800, 2800]),
    "emoji":  dict(ms=3000, taps=[1000, 2000]),
    "eyes":   dict(ms=2140),
    "flag":   dict(ms=2000, taps=[1000]),
    "heart":  dict(ms=1100),
    "life":   dict(ms=8000, seed=3),
    "name":   dict(ms=1840, seed=1),
    "rain": dict(ms=6000, seed=1),
    "stars":   dict(ms=6000, seed=1),
}

BASE_LEVEL = 0.05   # the board's default brightness, shown as full colour in the GIF
MIN_MS = 40         # frames closer together than this are merged (keeps GIFs small)

CELL = 48           # pixels per LED position
PAD = 24            # border around the matrix
SIZE = 5 * CELL + 2 * PAD
BOARD = (14, 14, 18)    # board background
UNLIT = (36, 36, 42)    # LED that is off


class Finished(BaseException):
    """Raised when the recording time is over; ends the app's endless loop."""


class Recorder:
    def __init__(self, ms, taps):
        self.now = 0
        self.end = ms
        self.taps = sorted(taps)
        self.events = []            # (time in ms, frame)

    def advance(self, ms):
        self.now += ms
        if self.now >= self.end:
            raise Finished

    def record(self, frame):
        if self.now >= self.end:
            raise Finished
        self.events.append((self.now, list(frame)))


def make_modules(rec):
    """Stand-ins for the board's time, ws2812 and touch modules."""
    t = types.ModuleType("time")
    t.sleep_ms = rec.advance
    t.sleep = lambda s: rec.advance(int(s * 1000))
    t.ticks_ms = lambda: int(rec.now)
    t.ticks_diff = lambda a, b: a - b
    t.ticks_add = lambda a, b: a + b

    w = types.ModuleType("ws2812")
    w.BRIGHTNESS = BASE_LEVEL
    w.OFF = (0, 0, 0)
    w.BLANK = [w.OFF] * 25

    def pack(r, g, b, level=None):
        # Real board: colour * level. Here the default level shows as the full
        # colour; dimmer or brighter levels scale from there, keeping the hue.
        level = w.BRIGHTNESS if level is None else level
        k = level / BASE_LEVEL
        top = max(r, g, b) * k
        if top > 255:
            k *= 255 / top
        return (int(r * k), int(g * k), int(b * k))

    def build_frame(rows, color, level=None):
        on = pack(color[0], color[1], color[2], level)
        return [on if ch == "#" else w.OFF for row in rows for ch in row]

    w.pack, w.build_frame, w.show = pack, build_frame, rec.record

    tm = types.ModuleType("touch")
    tm.POLL_MS = 10

    class Touch:
        def __init__(self, pins=None, debug=False):
            pass

        def tapped(self):
            if rec.taps and rec.now >= rec.taps[0]:
                rec.taps.pop(0)
                return True
            return False

    tm.Touch = Touch
    return {"time": t, "ws2812": w, "touch": tm}


def record(name, cfg):
    path = ROOT / "apps" / (name + ".py")
    if not path.exists():
        sys.exit("No such app file: %s" % path)
    rec = Recorder(cfg["ms"], cfg.get("taps", []))
    names = ("time", "ws2812", "touch")
    saved = {n: sys.modules.get(n) for n in names}
    sys.modules.update(make_modules(rec))
    random.seed(cfg.get("seed", 1))
    try:
        runpy.run_path(str(path), run_name="__main__")
    except Finished:
        pass
    finally:                        # put the real modules back
        for n, mod in saved.items():
            if mod is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = mod
    return rec.events


def render(frame, glow_on=True):
    img = Image.new("RGB", (SIZE, SIZE), BOARD)
    glow = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
    draw, gdraw = ImageDraw.Draw(img), ImageDraw.Draw(glow)
    r = CELL * 0.34
    lit = []
    for i, px in enumerate(frame):
        y, x = divmod(i, 5)
        cx = PAD + x * CELL + CELL / 2
        cy = PAD + y * CELL + CELL / 2
        if px != (0, 0, 0):
            lit.append((cx, cy, px))
            if glow_on:
                gdraw.ellipse((cx - r * 1.5, cy - r * 1.5, cx + r * 1.5, cy + r * 1.5), fill=px)
        else:
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=UNLIT)
    if glow_on:
        img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(9)))
    draw = ImageDraw.Draw(img)
    for cx, cy, px in lit:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=px)
    return img


def make_gif(name, cfg):
    events = record(name, cfg)
    if not events:
        sys.exit("%s never showed a frame" % name)

    kept = []                       # merge frames closer than MIN_MS; the last one wins
    for t, frame in events:
        if kept and t - kept[-1][0] < MIN_MS:
            kept[-1] = (kept[-1][0], frame)
        else:
            kept.append((t, frame))

    steps = []                      # [frame, how long it stays] with repeats merged
    for i, (t, frame) in enumerate(kept):
        end = kept[i + 1][0] if i + 1 < len(kept) else cfg["ms"]
        d = max(end - t, 20)
        if steps and steps[-1][0] == frame:
            steps[-1][1] += d
        else:
            steps.append([frame, d])

    images = [render(f, cfg.get("glow", True)) for f, _ in steps]
    durations = [int(round(d / 10.0) * 10) for _, d in steps]
    out = ROOT / "gifs" / (name + ".gif")
    out.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(out, save_all=True, append_images=images[1:],
                   duration=durations, loop=0)
    print("%-7s %3d frames  %6.1f s  %7d bytes  -> %s" % (
        name, len(images), sum(durations) / 1000.0, out.stat().st_size, out))


def main():
    names = sys.argv[1:]
    if not names:
        sys.exit("Usage: make_gif.py <app> [<app> ...] | all\nApps: " + " ".join(APPS))
    if names == ["all"]:
        names = list(APPS)
    for n in names:
        if n not in APPS:
            sys.exit("Unknown app %r. Known apps: %s" % (n, " ".join(APPS)))
    for n in names:
        make_gif(n, APPS[n])


if __name__ == "__main__":
    main()
