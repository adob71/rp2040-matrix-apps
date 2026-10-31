import sys
import time
import machine
import rp2

# Apps live in /apps on the board. Names = file names without ".py".
# Order = order of BOOTSEL presses.
APPS_DIR = "/apps"
APPS = ["avatar", "count", "dice", "emoji", "eyes", "flag", "heart", "life", "name", "rain", "stars"]
STATE_FILE = "app_index"      # remembers which app was running

def load_index():
    try:
        with open(STATE_FILE) as f:
            return int(f.read()) % len(APPS)
    except (OSError, ValueError):
        return 0

def save_index(i):
    with open(STATE_FILE, "w") as f:
        f.write(str(i))

index = load_index()

def next_app():
    save_index((index + 1) % len(APPS))
    machine.soft_reset()          # fresh PIO + RAM; main.py runs again

# Sleep functions that watch the BOOTSEL button.
# Long sleeps are sliced into 20 ms pieces so the button is checked often.
_sleep_ms = time.sleep_ms

def sleep_ms(ms):
    end = time.ticks_add(time.ticks_ms(), ms)
    while True:
        if rp2.bootsel_button():
            next_app()
        left = time.ticks_diff(end, time.ticks_ms())
        if left <= 0:
            return
        _sleep_ms(min(left, 20))

def sleep(s):
    sleep_ms(int(s * 1000))

# After a switch the button may still be held down: wait for release first
while rp2.bootsel_button():
    _sleep_ms(10)
_sleep_ms(100)

# The built-in time module is read-only, so register a stand-in under the name
# "time" that apps pick up when they "import time".
class _Time:
    pass

fake_time = _Time()
for _n in dir(time):
    if not _n.startswith("__"):
        setattr(fake_time, _n, getattr(time, _n))
fake_time.sleep_ms = sleep_ms
fake_time.sleep = sleep
sys.modules["time"] = fake_time

sys.path.append(APPS_DIR)         # lets "import dice" find /apps/dice.py

name = APPS[index]
print("launcher: starting %s (%d/%d)" % (name, index + 1, len(APPS)))
try:
    __import__(name)              # runs the app's top-level code
except Exception as e:
    sys.print_exception(e)
print("launcher: %s ended, press BOOTSEL for the next app" % name)
while True:                       # only reached if an app returns or crashes
    time.sleep_ms(50)
