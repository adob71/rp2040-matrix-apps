import time
import math
import random
import ws2812

NUM_LEDS = 25
STEP_MS = 30               # time between updates
TWINKLE_CHANCE = 0.02      # chance per step that a new twinkle starts
MAX_TWINKLING = 2          # most pixels twinkling at once
TWINKLE_MS = (500, 1000)   # min and max length of one twinkle
PEAK_LEVEL = (0.05, 0.12)  # min and max brightness at the top of a twinkle

TINTS = [
    (200, 210, 255),   # blue-white
    (255, 235, 200),   # warm white
    (190, 205, 255),   # pale blue
]

twinkles = {}   # pixel index -> (start ms, duration ms, peak level, tint)

while True:
    now = time.ticks_ms()

    # now and then, a random pixel starts to twinkle
    if len(twinkles) < MAX_TWINKLING and random.random() < TWINKLE_CHANCE:
        i = random.randint(0, NUM_LEDS - 1)
        if i not in twinkles:
            twinkles[i] = (now,
                           random.randint(*TWINKLE_MS),
                           random.uniform(*PEAK_LEVEL),
                           random.choice(TINTS))

    frame = [ws2812.OFF] * NUM_LEDS   # the sky is dark unless something twinkles
    for i, (start, dur, peak, tint) in list(twinkles.items()):
        t = time.ticks_diff(now, start) / dur
        if t >= 1:
            del twinkles[i]
        else:
            level = peak * math.sin(math.pi * t) ** 2
            frame[i] = ws2812.pack(tint[0], tint[1], tint[2], level)

    ws2812.show(frame)
    time.sleep_ms(STEP_MS)
