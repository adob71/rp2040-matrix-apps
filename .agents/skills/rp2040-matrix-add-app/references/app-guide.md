# RP2040-Matrix app guide

Reference for writing apps in `apps/`. It covers how an app runs, the rules every app follows, the
library calls and four patterns to start from.

## How an app runs

The launcher (`launcher.py`, installed on the board as `main.py`) imports `apps/<name>.py`. The
top-level code of that file is the app, and it must loop forever. Pressing BOOT restarts the board
on the next app in the `APPS` list, so every app starts from a clean state.

The launcher swaps in a `time` module whose sleep functions check the BOOT button. That is the only
way BOOT can interrupt an app, so the main loop must call `time.sleep_ms()` or `time.sleep()` on
every pass.

## The board

- 25 LEDs in a 5×5 grid, numbered row by row: `index = row * 5 + column`. Row 0 is the top row, with
  the USB-C connector at the top, and column 0 is on the left.
- Seven touch pads (GP8 to GP14) along the bottom edge. A touch on any of them counts.
- The LEDs use PIO state machine 0 and the touch pads use state machines 1 to 7, so apps must not
  use `machine` or `rp2` themselves.

## Rules

1. Import only `time`, `ws2812`, `touch`, `random` and `math`.
2. Sleep on every pass of the main loop. A loop that never sleeps cannot be interrupted by BOOT.
3. Never read the BOOT button in an app. The launcher does that.
4. Show something right away, before slow setup such as touch calibration, so the board is never
   dark after a switch.
5. Put settings in capitals at the top (`COLOR`, `DELAY_MS`) with a short comment, and avoid numbers
   buried in the code.
6. Keep touch apps responsive. Sleep `touch.POLL_MS` (10 ms) on each pass and use `time.ticks_ms()`
   timers for anything slower, as `apps/dice.py` does. A long sleep between frames makes touches
   feel laggy.
7. Colours are `(R, G, B)` with 0 to 255 per channel. The library applies a low brightness by
   default, so full-strength colours such as `(255, 0, 0)` are right.
8. Name the file in lowercase as a valid Python name, and never as `time`, `math`, `random`, `touch`
   or `ws2812`, or the name of another app. The launcher imports apps by name.

## `ws2812` library

| Call | What it does |
|---|---|
| `ws2812.build_frame(rows, color, level=None)` | Turns 5 strings of 5 characters (`#` lit, `.` off) into a frame in one colour. |
| `ws2812.pack(r, g, b, level=None)` | One pixel value, for frames built pixel by pixel. |
| `ws2812.show(frame)` | Sends a frame to the LEDs. A frame is a list of 25 pixel values. |
| `ws2812.OFF` | The value of a dark pixel. |
| `ws2812.BLANK` | A frame with every pixel off. |

`level` is the brightness from 0.0 to 1.0. The default is 0.05, and existing apps use levels up to
about 0.12. Two things follow:

- Leave `level` out for normal colours. The default is already bright.
- A dim colour with small numbers, such as `(10, 10, 10)`, goes completely dark at the default
  level, because every channel is multiplied by 0.05 and rounded down. Any channel below 20 is lost
  that way. Pass `level=1.0` for such colours, as `apps/count.py` and `apps/eyes.py` do.

To light single pixels, start from a dark frame:

```python
frame = [ws2812.OFF] * 25
frame[2 * 5 + 2] = ws2812.pack(255, 255, 255)   # row 2, column 2: the middle pixel
ws2812.show(frame)
```

## `touch` library

For apps that react to touch.

- `pad = touch.Touch()` is created once. It takes about a second to learn the untouched level, so
  show the first frame before it and keep fingers off the pads.
- `pad.tapped()` returns `True` once for each new touch on any pad, and is ready again after every
  finger has lifted. Call it on every pass of the loop.
- `touch.POLL_MS` is 10 and is the sleep to use in a touch app's loop.
- Do not use `pad.touched`. The preview tool does not support it.

## `time` calls

Use only `sleep_ms`, `sleep`, `ticks_ms`, `ticks_diff` and `ticks_add`. The preview tool supports no
others, and anything else raises an `AttributeError` there.

## Patterns to start from

### Fixed frames

```python
import time
import ws2812

COLOR = (0, 255, 0)      # (R, G, B)
DELAY_MS = 200           # time per frame

FRAMES = [
    ("#....", ".#...", "..#..", "...#.", "....#"),
    ("....#", "...#.", "..#..", ".#...", "#...."),
]

frames = [ws2812.build_frame(rows, COLOR) for rows in FRAMES]

while True:
    for frame in frames:
        ws2812.show(frame)
        time.sleep_ms(DELAY_MS)
```

### Touch changes the frame

```python
import time
import ws2812
import touch

COLOR = (255, 255, 0)

FRAMES = [
    ("..#..", ".###.", "#####", ".###.", "..#.."),
    ("#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
]

frames = [ws2812.build_frame(rows, COLOR) for rows in FRAMES]

index = 0
ws2812.show(frames[index])           # show something before the touch calibration
pad = touch.Touch()                  # about a second: keep fingers off the pads

while True:
    if pad.tapped():
        index = (index + 1) % len(frames)
        ws2812.show(frames[index])
    time.sleep_ms(touch.POLL_MS)
```

### Computed frames

```python
import time
import random
import ws2812

COLOR = (255, 255, 255)
STEP_MS = 100

while True:
    frame = [ws2812.OFF] * 25                 # all dark
    pixel = random.randrange(25)              # pick any pixel
    frame[pixel] = ws2812.pack(*COLOR)        # light it
    ws2812.show(frame)
    time.sleep_ms(STEP_MS)
```

### Touch plus timing

```python
import time
import random
import ws2812
import touch

COLOR = (0, 200, 255)
STEP_MS = 150                        # time between frames while running

ws2812.show(ws2812.BLANK)
pad = touch.Touch()
running = False
last = time.ticks_ms()

while True:
    if pad.tapped():
        running = not running        # touch starts and stops the animation
        last = time.ticks_ms()
    if running and time.ticks_diff(time.ticks_ms(), last) >= STEP_MS:
        last = time.ticks_ms()
        frame = [ws2812.OFF] * 25
        frame[random.randrange(25)] = ws2812.pack(*COLOR)
        ws2812.show(frame)
    time.sleep_ms(touch.POLL_MS)
```

## Preview entry in `tools/make_gif.py`

The `APPS` table at the top of `tools/make_gif.py` has one line per app:

```python
"traffic": dict(ms=7000),
"emoji":   dict(ms=3000, taps=[1000, 2000]),
"stars":   dict(ms=6000, seed=1),
```

- `ms` is how many milliseconds of the app to record. For a loop, use the time of one full cycle:
  for example 10 digits of 100 ms each is 1000, and a name of 6 letters at 240 ms each plus a 400 ms
  pause is 1840. For a touch app, record long enough to show every state.
- `taps` lists the times in milliseconds at which a touch is simulated. Space them about a second
  apart so that each state is visible.
- `seed` fixes the random numbers for apps that use `random`. Change it to get a different run.
- `glow=False` draws plain round LEDs and keeps the GIF small. Use it only for long, busy
  animations, because the glow is what makes the preview look like the real board.

The preview runs on a fake clock without the touch calibration, so it is fast and shows the colours
at full strength.

## Descriptions that work well

- "A traffic light: red for 3 seconds, then green for 3, then yellow for 1, drawn as a 3×3 block in
  the middle. No touch."
- "A white pixel that moves diagonally and bounces off the edges."
- "Touch to start and stop a stream of random blue pixels."

Anything from a single sentence to a full spec is fine. The more detail, the fewer assumptions.
