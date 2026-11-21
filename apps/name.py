import time
import random
import ws2812
import text

TEXT = "MATRIX"

BRIGHTNESS = 0.05

DELAY_MS = 200
GAP_MS = 40
END_MS = 400


def hue_to_rgb(h):
    """Convert hue (0.0–1.0) to RGB."""
    i = int(h * 6)
    f = h * 6 - i
    rising = int(255 * f)
    falling = int(255 * (1 - f))

    return [
        (255, rising, 0),
        (falling, 255, 0),
        (0, 255, rising),
        (0, falling, 255),
        (rising, 0, 255),
        (255, 0, falling),
    ][i % 6]


hue = random.random()


def next_color():
    """Return a random color at reduced brightness."""
    global hue
    hue = (hue + random.uniform(0.2, 0.8)) % 1.0

    return tuple(
        int(channel * BRIGHTNESS)
        for channel in hue_to_rgb(hue)
    )


while True:
    for ch in TEXT:
        ws2812.show(text.build_frame(ch, next_color()))
        time.sleep_ms(DELAY_MS)

        ws2812.show(ws2812.BLANK)
        time.sleep_ms(GAP_MS)

    time.sleep_ms(END_MS)
