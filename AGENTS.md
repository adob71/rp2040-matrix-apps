# RP2040-Matrix apps

Little MicroPython apps for the Waveshare RP2040-Matrix, a board with a 5×5 RGB LED matrix, touch pads and a BOOT button that steps through the apps. The board runs MicroPython v1.26.1. The tooling and skills assume macOS.

## Repository map

- `apps/` has one file per app. `launcher.py` is installed on the board as `main.py` and runs them one at a time.
- `lib/` has the shared code: `ws2812.py` for the LEDs and `touch.py` for the touch pads.
- `tools/make_gif.py` runs an app on the computer and records its preview GIF in `gifs/`.
- `docs/` has the board drawings, `firmware/` the MicroPython `.uf2` file, and `deploy.sh` copies everything to the board (`--firmware` or `--apps`).

## Skills

Use the skills in `.agents/skills/` for these tasks instead of improvising:

- `rp2040-setup` installs the tools and checks the USB connection, once per computer.
- `rp2040-add-app` adds an app and its preview. The app rules are in `.agents/skills/rp2040-add-app/references/app-guide.md`.
- `rp2040-deploy` flashes the firmware on a new board and deploys the apps.

## Rules

- Apps import only `time`, `ws2812`, `touch`, `random` and `math`, and sleep on every pass of their main loop. They never read the BOOT button or use `machine` or `rp2`.
- The `APPS` list in `launcher.py` and the table in `README.md` stay in alphabetical order.
- Ask before running `./deploy.sh --firmware` or deleting files on the board. Never leave `mpremote repl` open.
- Do not commit unless asked. Keep commit messages short and specific, such as `feat: add rp2040-deploy skill`.
- The README is for users and is written in British English ("colours"). Keep it short.
