"""
Usage:
    python3 tools/make_banner.py

Generates docs/banner.png from the 5x5 pixel font.
"""

from PIL import Image, ImageDraw, ImageFont
import os

TEXT = "RP2040-Matrix Apps"
FONT_PATH = "fonts/micro_chat_monospaced_5x5.ttf"
FONT_SIZE = 64
OUTPUT_PATH = "docs/banner.png"

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Calculate dimensions with padding (x: 16, y: 12)
dummy = Image.new("RGB", (1, 1))
bbox = ImageDraw.Draw(dummy).textbbox((0, 0), TEXT, font=font)
w = (bbox[2] - bbox[0]) + 32
h = (bbox[3] - bbox[1]) + 24

# Create solid black image and draw white text
img = Image.new("RGB", (w, h), (0, 0, 0))
ImageDraw.Draw(img).text((16 - bbox[0], 12 - bbox[1]), TEXT, font=font, fill=(255, 255, 255))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
img.save(OUTPUT_PATH)
print(f"Banner generated successfully -> {OUTPUT_PATH}")
