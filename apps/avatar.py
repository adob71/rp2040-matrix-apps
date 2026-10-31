import time
import ws2812

# Each identicon: (color as R, G, B, 5 rows where '#' = lit)
IDENTICONS = [
    ((135, 222, 230), [    # 1: cyan
        "#.#.#",
        "..#..",
        "..#..",
        ".###.",
        "#...#",
    ]),
    ((255, 235, 0), [      # 2: yellow
        ".###.",
        "#.#.#",
        ".....",
        ".#.#.",
        ".###.",
    ]),
    ((255, 40, 0), [       # 3: red
        "#...#",
        "##.##",
        "#####",
        "..#..",
        "##.##",
    ]),
    ((172, 222, 150), [    # 4: light green
        ".....",
        "##.##",
        ".....",
        "#####",
        "..#..",
    ]),
    ((168, 218, 105), [    # 5: green
        ".#.#.",
        ".#.#.",
        "#####",
        ".....",
        "##.##",
    ]),
]

frames = [ws2812.build_frame(rows, color) for color, rows in IDENTICONS]

while True:
    for frame in frames:
        ws2812.show(frame)
        time.sleep(2)
