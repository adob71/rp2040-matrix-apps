import time
import ws2812
import touch

RED = (255, 0, 0)   # (R, G, B)

FLAG = (".#...",
        ".##..",
        ".###.",
        ".##..",
        ".#...")

frames = [ws2812.BLANK,                       # 0 = blank
          ws2812.build_frame(FLAG, RED)]      # 1 = red flag

ws2812.show(frames[0])                        # start blank
pad = touch.Touch(debug=False)                # learns untouched levels: keep fingers off
index = 0

while True:
    if pad.tapped():
        index = (index + 1) % len(frames)
        ws2812.show(frames[index])
    time.sleep_ms(touch.POLL_MS)
