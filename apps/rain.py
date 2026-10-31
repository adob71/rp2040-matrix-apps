import time
import math
import random
import ws2812

ROWS = COLS = 5
BRIGHTNESS = 0.08          # 0.0 - 1.0 (this app's own brightness, separate from ws2812.BRIGHTNESS)
STEP_MS = 70               # time per step (lower = faster rain)
HEAD = (170, 255, 170)     # (R, G, B) bright head of each streak
TAIL = (0, 255, 60)        # (R, G, B) green trail
SPEED = (0.25, 0.8)        # min and max fall speed in rows per step
TAIL_LEN = (2, 4)          # min and max trail length in pixels
MAX_DELAY = 8              # most steps a column waits before a new streak

def pack(color, level):
    return ws2812.pack(color[0], color[1], color[2], BRIGHTNESS * level)

def new_drop():
    # [head row (negative = still above the matrix), speed, tail length]
    return [-random.uniform(0, MAX_DELAY),
            random.uniform(*SPEED),
            random.randint(*TAIL_LEN)]

drops = [new_drop() for _ in range(COLS)]

while True:
    frame = [ws2812.OFF] * (ROWS * COLS)
    for c in range(COLS):
        head, speed, tail = drops[c]
        head_row = math.floor(head)
        for t in range(tail + 1):
            r = head_row - t
            if 0 <= r < ROWS:
                if t == 0:
                    frame[r * COLS + c] = pack(HEAD, 1.0)
                else:
                    # fade along the tail, with a little random flicker
                    level = (1 - t / (tail + 1)) * random.uniform(0.6, 1.0)
                    frame[r * COLS + c] = pack(TAIL, level)
        drops[c][0] += speed
        if head_row - tail >= ROWS:     # streak has left the matrix
            drops[c] = new_drop()

    ws2812.show(frame)
    time.sleep_ms(STEP_MS)
