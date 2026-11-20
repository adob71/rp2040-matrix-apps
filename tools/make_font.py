#!/usr/bin/env python3
"""Convert Micro Chat TTF glyphs into 5x5 MicroPython bitmap data."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

FONT = ROOT / "fonts/Micro_Chat_Monospaced_5x5.ttf"
OUTPUT = ROOT / "lib/font.py"

SIZE = 5

CHARACTERS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    " !#$%()*+-./:<=>?[]_|~@"
)

font = ImageFont.truetype(str(FONT), SIZE)
glyphs = {}

for char in CHARACTERS:
    bbox = font.getbbox(char)

    image = Image.new("1", (max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])))
    ImageDraw.Draw(image).text((-bbox[0], -bbox[1]), char, font=font, fill=1)

    # Remove empty borders.
    bounds = image.getbbox()

    cell = Image.new("1", (SIZE, SIZE))

    if bounds:
        image = image.crop(bounds)

        # Fit glyph proportionally inside the 5x5 cell.
        image.thumbnail((SIZE, SIZE), Image.Resampling.NEAREST)

        # Centre horizontally and align to the bottom baseline.
        x = (SIZE - image.width) // 2
        y = SIZE - image.height
        cell.paste(image, (x, y))

    glyphs[char] = tuple(
        "".join("#" if cell.getpixel((x, y)) else "." for x in range(SIZE))
        for y in range(SIZE)
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w") as f:
    f.write('"""Generated font data. Do not edit manually."""\n\n')
    f.write("GLYPHS = {\n")

    for char, bitmap in glyphs.items():
        f.write(f"    {char!r}: {bitmap!r},\n")

    f.write("}\n")

print(f"Generated {len(glyphs)} glyphs : {OUTPUT}")
