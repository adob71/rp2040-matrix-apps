# RP2040-Matrix apps

Little MicroPython apps for the Waveshare RP2040-Matrix, a board with a 5×5 RGB LED matrix, touch pads and a BOOT button that steps through the apps. The board runs the MicroPython version of the `.uf2` file in `firmware/`. The tooling and skills assume macOS.

## Repository map

- `apps/` has one file per app. `launcher.py` is installed on the board as `main.py` and runs them one at a time.
- `lib/` has the shared code: `ws2812.py` for the LEDs and `touch.py` for the touch pads.
- `tools/make_preview.py` runs an app on the computer and records its preview GIF in `preview/`.
- `docs/` has the board drawings, `firmware/` the MicroPython `.uf2` file, and `deploy.sh` copies everything to the board (`--firmware` or `--apps`).
- `preview/` has the app preview GIFs, `demo/` the demo GIFs, `fonts/` the pixel font used by the tools, and `tools/` the preview, demo and banner scripts.

## Skills

Use the skills in `.agents/skills/` for these tasks instead of improvising:

- `rp2040-matrix-setup` installs the tools, checks the USB connection and creates the preview `.venv`. Run it once per computer, and again in each new clone.
- `rp2040-matrix-add-app` adds an app and its preview. The app rules are in `.agents/skills/rp2040-matrix-add-app/references/app-guide.md`.
- `rp2040-matrix-deploy` flashes the firmware on a new board and deploys the apps.

## Rules

- Apps import only `time`, `ws2812`, `touch`, `random` and `math`, and sleep on every pass of their main loop. They never read the BOOT button or use `machine` or `rp2`.
- The `APPS` list in `launcher.py` and the table in `README.md` stay in alphabetical order.
- Ask before running `./deploy.sh --firmware` or deleting files on the board. Never leave `mpremote repl` open.
- Do not commit unless asked. Use Conventional Commits with one short, specific line, such as `feat(skills): add rp2040-matrix-deploy skill`.
- The README is for users and is written in British English ("colours"). Keep it short.
