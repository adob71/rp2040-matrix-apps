import time
import random
import ws2812
import touch

DEBUG = False                  # True prints touch values and the stopped face over USB serial

DICE_COLOR = (255, 255, 255)   # (R, G, B)
ROLL_MS = 80                   # time between faces while rolling

FACES = [
    (".....",   # 1
     ".....",
     "..#..",
     ".....",
     "....."),
    ("#....",   # 2
     ".....",
     ".....",
     ".....",
     "....#"),
    ("#....",   # 3
     ".....",
     "..#..",
     ".....",
     "....#"),
    ("#...#",   # 4
     ".....",
     ".....",
     ".....",
     "#...#"),
    ("#...#",   # 5
     ".....",
     "..#..",
     ".....",
     "#...#"),
    ("#...#",   # 6
     ".....",
     "#...#",
     ".....",
     "#...#"),
]

frames = [ws2812.build_frame(rows, DICE_COLOR) for rows in FACES]

face = 5                              # index 5 = the six, so it always starts on it
ws2812.show(frames[face])
pad = touch.Touch(debug=DEBUG)        # learns untouched levels: keep fingers off

rolling = False                       # waits on the 6; first tap starts the roll
last_roll = time.ticks_ms()

while True:
    if pad.tapped():
        rolling = not rolling
        last_roll = time.ticks_ms()
        if DEBUG:
            print("rolling" if rolling else "stopped on %d" % (face + 1))

    if rolling and time.ticks_diff(time.ticks_ms(), last_roll) >= ROLL_MS:
        last_roll = time.ticks_ms()
        new_face = random.randrange(len(frames) - 1)
        face = new_face if new_face < face else new_face + 1   # never the same face twice in a row
        ws2812.show(frames[face])

    time.sleep_ms(touch.POLL_MS)
