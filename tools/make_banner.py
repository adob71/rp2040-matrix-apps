#!/usr/bin/env python3
"""Generate docs/banner.png (1280x640) for the GitHub social preview.

Usage: python3 tools/make_banner.py
"""

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "fonts/mono_regular_3x5_blocked.ttf"
OUTPUT_PATH = "docs/banner.png"
W, H = 1280, 640

img = Image.new("RGB", (W, H), "black")
draw = ImageDraw.Draw(img)


def centered(y, text, size, fill):
    # Sizes that are multiples of 6 keep the 3x5 pixels sharp; shrink until it fits.
    while True:
        font = ImageFont.truetype(FONT_PATH, size)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        if right - left <= W - 160 or size <= 6:
            break
        size -= 6
    draw.text(((W - (right - left)) // 2 - left, y - top), text, font=font, fill=fill)


centered(220, "RP2040-Matrix Apps", 96, "white")
centered(380, "Little apps for a little LED matrix computer", 30, (150, 150, 150))
img.save(OUTPUT_PATH)
print(f"Saved {OUTPUT_PATH}")
