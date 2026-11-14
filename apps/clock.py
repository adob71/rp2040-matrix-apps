import time
import ws2812

HOUR_STEPS = 12                  # one full turn of the hour hand
SIM_STEPS_PER_SECOND = 12        # one simulated hour passes each real second
CHECK_MS = 10                    # check often enough for smooth steps
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HAND_ENDS = [
    (2, 0), (3, 1), (4, 0), (4, 2), (3, 3), (4, 4),
    (2, 4), (1, 3), (0, 4), (0, 2), (1, 1), (0, 0),
]                                # 12 clock positions on the 5x5 grid


def hand_pixels(step):
    # Trace the grid pixels from the centre to this clock position.
    end_x, end_y = HAND_ENDS[step % 12]
    dx = end_x - 2
    dy = end_y - 2
    count = max(abs(dx), abs(dy))
    pixels = []
    for part in range(1, count + 1):
        x = 2 + round(dx * part / count)
        y = 2 + round(dy * part / count)
        pixels.append(y * 5 + x)
    return pixels


def show_clock(minute_step):
    frame = [ws2812.OFF] * 25
    hour_step = (minute_step // HOUR_STEPS) % 12
    for pixel in hand_pixels(hour_step):
        frame[pixel] = ws2812.pack(*RED)
    for pixel in hand_pixels(minute_step):
        frame[pixel] = ws2812.pack(*BLUE)
    frame[12] = ws2812.pack(255, 255, 255)
    ws2812.show(frame)


minute_step = 0
last_check = time.ticks_ms()
step_phase = 0
show_clock(minute_step)

while True:
    now = time.ticks_ms()
    elapsed = time.ticks_diff(now, last_check)
    last_check = now
    step_phase += elapsed * SIM_STEPS_PER_SECOND
    steps = step_phase // 1000
    step_phase %= 1000
    if steps:
        minute_step = (minute_step + steps) % (HOUR_STEPS * HOUR_STEPS)
        show_clock(minute_step)
    time.sleep_ms(CHECK_MS)
