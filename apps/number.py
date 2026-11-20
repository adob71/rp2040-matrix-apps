import time
import ws2812
import text

COLOR = (6, 6, 6)
DELAY_MS = 100

while True:
    for digit in "0123456789":
        frame = text.build_frame(digit, COLOR, level=1.0)
        ws2812.show(frame)
        time.sleep_ms(DELAY_MS)
