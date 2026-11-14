from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
TEXT = "RP2040-Matrix Apps"
FONT_PATH = "fonts/Everyday_Slight_5x5_Pixel_Font.ttf"  # Path to your downloaded font
FONT_SIZE = 32                      # Adjust based on font scaling
OUTPUT_PATH = "fonts/header.png"

# Load font
try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except IOError:
    print(f"Font not found at {FONT_PATH}")
    exit(1)

# Calculate text size using modern Pillow bounding box method
dummy_img = Image.new("RGBA", (1, 1))
draw = ImageDraw.Draw(dummy_img)
bbox = draw.textbbox((0, 0), TEXT, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Add padding
padding_x = 16
padding_y = 12
img_width = text_width + (padding_x * 2)
img_height = text_height + (padding_y * 2)

# Create transparent image (or match GitHub background: dark/light friendly or transparent)
img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw text (adjust color as needed, e.g., white text for dark mode or specific hex)
draw.text((padding_x - bbox[0], padding_y - bbox[1]), TEXT, font=font, fill=(255, 255, 255, 255))

# Save output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
img.save(OUTPUT_PATH, "PNG")
print(f"Header generated successfully -> {OUTPUT_PATH}")
