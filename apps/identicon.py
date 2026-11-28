import time
import ws2812
import touch

DEBUG = False                  # True prints touch values and the identicon number over USB serial

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
    ((220, 220, 220), [    # 6: white
        "..#..",
        ".###.",
        "..#..",
        "..#..",
        "..#..",
    ]),
    ((255, 170, 0), [    # 7: gold
        ".###.",
        "..#..",
        ".###.",
        "..#..",
        "##.##",
    ]),
]

frames = [ws2812.build_frame(rows, color) for color, rows in IDENTICONS]

index = 0                             # start with the first identicon
ws2812.show(frames[index])
pad = touch.Touch(debug=DEBUG)        # learns untouched levels: keep fingers off

while True:
    if pad.tapped():
        index = (index + 1) % len(frames)
        ws2812.show(frames[index])
        if DEBUG:
            print("identicon", index)

    time.sleep_ms(touch.POLL_MS)
