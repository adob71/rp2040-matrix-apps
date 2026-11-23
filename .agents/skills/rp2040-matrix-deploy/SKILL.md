---
name: rp2040-matrix-deploy
description: >-
  Deploys the RP2040-Matrix apps to the board on macOS. Installs MicroPython
  firmware on a brand-new board (every new Waveshare board needs it once; hold
  BOOT while plugging in) and copies the launcher, library and apps with
  deploy.sh. Use when the user wants to deploy, upload, flash, install
  firmware, update the board or see a new or changed app on the board, and
  after adding or editing an app. Needs the setup from rp2040-matrix-setup to
  be done first.
compatibility: macOS, mpremote and an RP2040-Matrix board connected over USB with a data cable.
---

# Deploy to the RP2040-Matrix board

The goal is to install the repository firmware if needed and deploy the launcher, the library and
the apps to the board.

Keep the deployment simple and follow the steps in order. Stop at the first failure unless a step
says to continue. Run commands yourself. A request to deploy counts as permission to restart the
board and stop the running app, so do not ask again before `./deploy.sh --apps` or
`mpremote reset`. Ask first before flashing firmware, before deleting anything from the board and
before running any command this skill does not list.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

If a command fails because your command sandbox blocks the network, USB access or files outside the
repository, ask permission to run it outside the sandbox and repeat it. Escalate only that one
command.

Placeholders in angle brackets, such as `<app-name>`, stand for real values. Write them without the
angle brackets.

## 1. Check the basics

Check that `deploy.sh`, `launcher.py`, `apps/` and `lib/` exist, and that `command -v mpremote`
finds mpremote. If mpremote is missing, stop and send the user to the `rp2040-matrix-setup` skill.

## 2. Find out what state the board is in

Run these checks:

```bash
[ -d /Volumes/RPI-RP2 ] && echo "BOOTSEL volume present" || echo "BOOTSEL volume absent"
mpremote connect list
```

Run `mpremote exec "import sys; print(sys.version)" 2>&1 | tail -n 15` only when no BOOTSEL volume
is present and `connect list` shows exactly one `usbmodem` device. If it shows more than one, ask
which is the board and use `mpremote connect <port> exec ...` instead. This check may soft-reset the
board and stop the running app. Deploying already replaces that app, so it needs no extra
permission. The `tail` keeps the output short, because a board running the factory test floods it.

Then read the results:

| Result | Meaning | Next |
|---|---|---|
| `/Volumes/RPI-RP2` exists | The board is in BOOTSEL mode. It may be new, or a working board that was put in BOOTSEL mode | Ask the user: flash MicroPython now (go to step 3), or unplug and reconnect without BOOT to check whether MicroPython is already installed (repeat step 2). If this session already showed that the board blocks the REPL, skip the reconnect option and go straight to step 3 |
| A MicroPython version is printed | The board is ready | Go to step 4 |
| `connect list` shows a `usbmodem` device, but `mpremote exec` says "no device found" | Your command sandbox is blocking the serial port, so the board is fine | Ask for permission to run the command outside the sandbox and repeat it. Do not blame the cable |
| `connect list` shows a `usbmodem` device, but `mpremote exec` fails with "could not enter raw repl", and the output is a repeating stream such as "GPIO test" and "ADC test" lines | The board runs a program that never lets the REPL in. On a new board this is the Waveshare factory test, which is normal. RESET only restarts it | Do not retry, and do not suggest RESET, reconnecting or closing serial programs. Tell the user the board is new and needs MicroPython installed, then go to step 3 |
| No drive and no `usbmodem` device | The board is not connected, the cable carries no data, or the board runs other firmware without USB | Ask the user to reconnect it with a data cable, try another port and repeat the checks. If there is still nothing, ask them to hold BOOT while plugging in, then go to step 3 |

If the user explicitly asks to reinstall or upgrade the firmware, go to step 3 even when MicroPython
answers.

## 3. Install the firmware (every new board, and recovery)

This is for a brand-new board, a board without MicroPython, or an upgrade the user asked for. Before
flashing, explain that it replaces MicroPython and may erase files stored on the board. Files from
this repository come back with step 4, but anything else on the board would be lost. If the board
showed the factory test, say that flashing replaces only the factory program and there is nothing
else on the board to lose. Get an explicit yes first.

a) Ask the user to put the board in BOOTSEL mode: unplug the USB cable, hold the BOOT button, plug
   the cable in, then release BOOT. If the board is already plugged in, holding BOOT and pressing
   RESET also works. Wait for their confirmation, then check `ls /Volumes/RPI-RP2`. If the drive
   does not appear, try another cable or port, and make sure BOOT is held while plugging in.
b) Run `./deploy.sh --firmware`. It copies the `.uf2` file from `firmware/` to the board, waits up
   to ten seconds for the board to restart and lists its files. macOS may show a "disk not ejected
   properly" notice, which can be ignored.

If the output contains `Operation not permitted` or another copy error, the command sandbox may be
blocking access to the firmware volume. Ask permission to run the command outside the sandbox and
repeat it. Do not troubleshoot this as a board restart problem.

c) If the script reports that the board did not come back and there was no firmware copy error, wait
   a few seconds and repeat the MicroPython check from step 2. If the board still does not respond,
   ask the user to unplug and reconnect it. If the same "could not enter raw repl" failure or the
   factory output is still there after flashing, stop and report it. Do not loop.
d) Continue with the next top-level step, 4. Deploy the apps.

## 4. Deploy the apps

Before the first deploy in this session, run `mpremote fs ls`. The script overwrites `main.py`,
`lib/` and `apps/`. If the board holds other files, tell the user and ask before continuing.

Run `./deploy.sh --apps`. It copies `launcher.py` as `main.py`, then `lib/` and `apps/`, resets the
saved app so the board starts on the first one, prints the file lists and restarts the board. The
script prints every command it runs. Summarise the result and ignore the "File exists" lines from
`mkdir`, which are harmless.

Check the command exit status and output. The script exits with a non-zero status if a required
deployment command fails. If deployment fails, check the USB connection and whether the command
sandbox can access the serial port. Ask permission to retry outside the sandbox if necessary.

Report success only after confirming that the launcher, `lib/` and the apps are present on the
board.

## 5. Verify

- Compare the printed `:apps` and `:lib` file lists with the repository. Report missing files. Run
  `mpremote fs ls :apps` or `mpremote fs ls :lib` yourself only if the output was cut off or
  unclear.
- The script copies files but never deletes them. A file on the board with no match in `apps/` or
  `lib/`, for example an app that was renamed or removed, is stale. List such files and offer to
  remove them with `mpremote fs rm :apps/<app-name>.py`. Ask before removing anything.
- Check that every name in the `APPS` list in `launcher.py` has a file in `apps/`.
- Ask the user to look at the board. The first app should be running, and BOOT should step to the
  next one.

## Jump to a specific app

After a deploy the board starts on the first app. To go straight to another one, read the `APPS`
list in `launcher.py`, count the app's position from 0 and confirm that `launcher.py` saves the
current app in a file named `app_index`. Then run:

```bash
N=7   # replace 7 with the app's position in APPS, counting from 0
mpremote exec "open('app_index','w').write('$N')"
mpremote reset
```

The board then starts on that app until the next deploy.

## Rules

- Never run `./deploy.sh --firmware` without an explicit yes from the user and without
  `/Volumes/RPI-RP2` present.
- Never delete files from the board without asking.
- Never answer "could not enter raw repl" with RESET, a reconnect or closing serial programs. Those
  fix a busy port, not a program that blocks the REPL.
- Do not run `mpremote repl`. It keeps the USB port busy and blocks later commands. If a command
  reports a busy port, ask the user to close other serial programs such as Thonny, a serial monitor
  or another mpremote session.
- If the board shows nothing after a deploy, ask the user to press RESET. If it stays dark, suggest
  running the `rp2040-matrix-setup` skill again.
- To upgrade MicroPython, replace the `.uf2` file in `firmware/` and update `FIRMWARE_FILE` at the
  top of `deploy.sh`.
