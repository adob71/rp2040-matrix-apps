import time
import math
import ws2812

COLOR = (235, 60, 20)   # (R, G, B) red-orange like the picture
MIN_LEVEL = 0.01        # brightness between beats (0.0 - 1.0)
MAX_LEVEL = 0.08        # brightness at the peak of a beat, keep low
CYCLE_MS = 1100         # length of one heartbeat cycle
STEP_MS = 20            # time between brightness updates

HEART = (
    ".#.#.",
    "#####",
    "#####",
    ".###.",
    "..#..",
)

def beat(t):
    # t = position in the cycle, 0.0 - 1.0: a strong "lub" then a softer "dub"
    lub = math.exp(-((t - 0.12) / 0.06) ** 2)
    dub = 0.6 * math.exp(-((t - 0.32) / 0.07) ** 2)
    return min(1.0, lub + dub)

def draw(level):
    ws2812.show(ws2812.build_frame(HEART, COLOR, level))

while True:
    start = time.ticks_ms()
    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start)
        if elapsed >= CYCLE_MS:
            break
        level = MIN_LEVEL + (MAX_LEVEL - MIN_LEVEL) * beat(elapsed / CYCLE_MS)
        draw(level)
        time.sleep_ms(STEP_MS)
