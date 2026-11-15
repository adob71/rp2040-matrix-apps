import time
import ws2812

COLOR = (6, 6, 6)   # (R, G, B) dim soft white, used as-is (level=1.0 means no extra scaling)
DELAY_MS = 100      # time per digit; 100 = 10 digits per second

# 3x5 digits, read from the attached font image
DIGITS = [
    (".##", "#.#", "#.#", "#.#", "##."),   # 0
    (".#.", "##.", ".#.", ".#.", ".#."),   # 1
    ("##.", "..#", ".#.", "#..", "###"),   # 2
    ("##.", "..#", ".#.", "..#", "##."),   # 3
    ("#.#", "#.#", "###", "..#", "..#"),   # 4
    ("###", "#..", "###", "..#", "##."),   # 5
    (".#.", "#..", "##.", "#.#", ".#."),   # 6
    ("###", "..#", ".#.", ".#.", ".#."),   # 7
    (".#.", "#.#", ".#.", "#.#", ".#."),   # 8
    (".#.", "#.#", ".##", "..#", ".#."),   # 9
]

def digit_frame(rows):
    # center the 3-wide digit in the 5-wide matrix: one blank column each side
    wide = ["." + row + "." for row in rows]
    return ws2812.build_frame(wide, COLOR, level=1.0)

frames = [digit_frame(rows) for rows in DIGITS]

while True:
    for frame in frames:
        ws2812.show(frame)
        time.sleep_ms(DELAY_MS)
