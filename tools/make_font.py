#!/usr/bin/env python3
"""Convert a 3x5 pixel TTF into 5x5 MicroPython bitmap glyphs (lib/font.py).

Usage: python3 tools/make_font.py   (edit FONT below to pick blocked/notched/rounded)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts/mono_regular_3x5_blocked.ttf"  # or _notched.ttf / _rounded.ttf
OUTPUT = ROOT / "lib/font.py"
CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    " !#$%()*+-./:<=>?[]_|~@"
)

# Em size where "H" is exactly 5 px tall (the font's native pixel size).
size = next(s for s in range(4, 33)
            if ImageFont.truetype(str(FONT), s).getbbox("H", anchor="ls")[1] == -5)
font = ImageFont.truetype(str(FONT), size)

lines = []
for c in CHARS:
    img = Image.new("1", (5, 5))
    # Baseline at row 5, x=1 -> a 3-wide glyph lands in columns 1..3.
    ImageDraw.Draw(img).text((1, 5), c, font=font, fill=1, anchor="ls")
    rows = tuple("".join("#" if img.getpixel((x, y)) else "." for x in range(5)) for y in range(5))
    lines.append(f"    {c!r}: {rows!r},")

OUTPUT.write_text(
    '"""Generated font data. Do not edit manually."""\n\nGLYPHS = {\n' + "\n".join(lines) + "\n}\n"
)
print(f"Generated {len(CHARS)} glyphs (em size {size}) : {OUTPUT}")