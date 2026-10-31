import time
import ws2812
import touch

DEBUG = False                  # True prints touch values and the face number over USB serial

GREEN = (0, 255, 0)            # (R, G, B)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

EYES = (".....",
        ".#.#.",
        ".....")

FACES = [
    (GREEN,  EYES + ("#...#",    # smile
                     ".###.")),
    (YELLOW, EYES + ("#####",    # neutral
                     ".....")),
    (RED,    EYES + (".###.",    # frown
                     "#...#")),
]

frames = [ws2812.build_frame(rows, color) for color, rows in FACES]

index = 0                             # start with the smile
ws2812.show(frames[index])
pad = touch.Touch(debug=DEBUG)        # learns untouched levels: keep fingers off

while True:
    if pad.tapped():
        index = (index + 1) % len(frames)
        ws2812.show(frames[index])
        if DEBUG:
            print("face", index)

    time.sleep_ms(touch.POLL_MS)
