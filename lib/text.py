"""5x5 text rendering using the bitmap font."""

import font
import ws2812

FONT = font.GLYPHS

BLANK = (
    ".....",
    ".....",
    ".....",
    ".....",
    ".....",
)


def get_glyph(char):
    """Return the 5x5 bitmap for a character."""
    if not char:
        return BLANK

    return FONT.get(char[0], BLANK)

def build_frame(char, color, level=1.0):
    """Build a WS2812 frame for a single character."""
    glyph = get_glyph(char)
    return ws2812.build_frame(glyph, color, level=level)
