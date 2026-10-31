import time
from machine import Pin
import rp2

TOUCH_PINS = (8, 9, 10, 11, 12, 13, 14)  # GPIO numbers of the holes you touch (max 7)
FIRST_SM = 1            # state machine 0 belongs to the LEDs

MAX_COUNT = 5000        # give up measuring after this many loops (about 80 us)
CAL_SAMPLES = 50        # readings used to learn each pad's untouched level and noise
MIN_RISE = 3            # smallest rise over the untouched level that counts as a touch
NOISE_MULT = 3          # touch must also exceed this many times the pad's noise range
RELEASE_FRAC = 0.5      # a touch ends when the rise falls below this fraction of the trigger
CONFIRM = 2             # consecutive touched polls needed (filters noise)
POLL_MS = 10            # suggested time between polls (apps use it for their sleep)
AVG = 8                 # measurements averaged per reading

# Measure how long a pad takes to charge through the pin's internal pull-up.
# A finger on the pad adds capacitance, so charging takes longer (bigger count).
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW)
def _touch_pio():
    pull(block)                 # wait for Python to ask for a measurement
    mov(x, osr)                 # x = the maximum count Python sent
    set(pindirs, 1)             # pin as output ...
    set(pins, 0)                # ... driven low: discharge the pad
    nop()[31]
    nop()[31]
    set(pindirs, 0)             # pin as input: the pull-up now charges the pad
    label("count")
    jmp(pin, "done")            # stop as soon as the pin reads high
    jmp(x_dec, "count")
    label("done")
    mov(isr, x)
    push(block)

def _measure(s):
    s.put(MAX_COUNT)
    raw = s.get()
    return MAX_COUNT - raw if raw <= MAX_COUNT else MAX_COUNT

def _read(s):
    return sum(_measure(s) for _ in range(AVG)) / AVG

class Touch:
    def __init__(self, pins=TOUCH_PINS, debug=False):
        self.pins = pins
        self.debug = debug
        self.n = len(pins)
        self.pads = [Pin(p, Pin.IN, Pin.PULL_UP) for p in pins]
        self.sms = []
        for i, pad in enumerate(self.pads):
            s = rp2.StateMachine(FIRST_SM + i, _touch_pio, freq=125_000_000,
                                 set_base=pad, jmp_pin=pad)
            s.active(1)
            self.sms.append(s)

        # learn each pad's untouched level and noise (keep fingers off the pads)
        time.sleep_ms(500)
        samples = [[] for _ in range(self.n)]
        for _ in range(CAL_SAMPLES):
            for i in range(self.n):
                samples[i].append(_read(self.sms[i]))
            time.sleep_ms(10)
        self.base = [sum(s) / len(s) for s in samples]
        self.rise = [max(MIN_RISE, NOISE_MULT * (max(s) - min(s))) for s in samples]
        if debug:
            print("untouched levels:", [round(b, 1) for b in self.base])
            print("touch triggers at:", [round(b + r, 1) for b, r in zip(self.base, self.rise)])

        self.state = [False] * self.n   # per pad: currently touched?
        self.touched = []               # GPIO numbers touched right now
        self.hits = 0                   # consecutive polls with a touch
        self.armed = True               # True again once every finger is lifted
        self.tick = 0

    def tapped(self):
        """Call once per loop. True exactly once for each new touch."""
        values = [_read(s) for s in self.sms]

        for i in range(self.n):
            dev = values[i] - self.base[i]
            if self.state[i]:
                if dev < self.rise[i] * RELEASE_FRAC:
                    self.state[i] = False
            elif dev > self.rise[i]:
                self.state[i] = True
            if not self.state[i]:   # follow drift: quickly down, slowly up
                self.base[i] += dev * (0.2 if dev < 0 else 0.01)

        self.touched = [self.pins[i] for i in range(self.n) if self.state[i]]

        if self.touched:
            self.hits += 1
        else:
            self.hits = 0
            self.armed = True

        if self.debug:
            self.tick += 1
            if self.tick % 10 == 0:
                print([round(v) for v in values], self.touched)

        if self.hits >= CONFIRM and self.armed:
            self.armed = False
            if self.debug:
                print("tap on GP", self.touched)
            return True
        return False
