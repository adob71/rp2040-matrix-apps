import time
import ws2812

Y = (8, 8, 0)   # (R, G, B) yellow, used as-is (level=1.0 means no extra scaling)

# LED index in the 5x5 grid = row * 5 + column
MOUTH = (15, 19, 21, 22, 23)

EYES = {
    "single": (6, 8),         # one dot per eye
    "double": (1, 3, 6, 8),   # extra dot above each eye = raised eyebrows
}

def build_frame(eye_leds):
    on = ws2812.pack(Y[0], Y[1], Y[2], level=1.0)
    frame = [ws2812.OFF] * 25
    for i in MOUTH + eye_leds:
        frame[i] = on
    return frame

frames = {name: build_frame(leds) for name, leds in EYES.items()}

# (frame name, how long to hold it in ms)
SEQUENCE = [
    ("single", 1500),   # resting
    ("double",  200),   # quick raise
    ("single",  120),   # quick drop
    ("double",  200),   # second raise
    ("single",  120),
]

while True:
    for name, hold in SEQUENCE:
        ws2812.show(frames[name])
        time.sleep_ms(hold)
