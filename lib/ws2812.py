import time
from machine import Pin
import rp2

PIN = 16               # GPIO of the LED data line
BRIGHTNESS = 0.05      # 0.0 - 1.0 (apps may override: ws2812.BRIGHTNESS = 0.1)
SERPENTINE = False     # True if odd rows are wired right-to-left

OFF = 0
BLANK = [OFF] * 25

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def _ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    wrap()

_sm = rp2.StateMachine(0, _ws2812, freq=8_000_000, sideset_base=Pin(PIN))
_sm.active(1)

def pack(r, g, b, level=None):
    """One pixel as a 24-bit value; level defaults to BRIGHTNESS."""
    if level is None:
        level = BRIGHTNESS
    r, g, b = int(r * level), int(g * level), int(b * level)
    return (r << 24) | (g << 16) | (b << 8)   # RGB byte order for these LEDs

def build_frame(rows, color, level=None):
    """Turn 5 strings of '#' and '.' into a list of 25 pixels in one color."""
    on = pack(color[0], color[1], color[2], level)
    frame = []
    for y, row in enumerate(rows):
        if SERPENTINE and y % 2 == 1:
            row = row[::-1]
        frame.extend(on if ch == "#" else OFF for ch in row)
    return frame

def show(frame):
    for px in frame:
        _sm.put(px)
    time.sleep_ms(1)  # latch
