---
name: rp2040-matrix-deploy
description: >-
  Deploys the RP2040-Matrix apps to the board on macOS. Installs MicroPython
  firmware on a brand-new board (rare, needs BOOT held while plugging in) and
  copies the launcher, library and apps with deploy.sh. Use when the user wants
  to deploy, upload, flash, install firmware, update the board or see a new or
  changed app on the board, and after adding or editing an app. Needs the setup
  from rp2040-matrix-setup to be done first.
compatibility: macOS, mpremote and an RP2040-Matrix board connected over USB with a data cable.
---

# Deploy to the RP2040-Matrix board

Put the launcher, the library and the apps of this repository on the board. Work from the repository root, run commands yourself and stop at the first failure. Deploying restarts the board and stops the running app, which is expected. This skill is for macOS only.

## 1. Check the basics

Check that `deploy.sh`, `launcher.py`, `apps/` and `lib/` exist, and that `command -v mpremote` finds mpremote. If mpremote is missing, stop and send the user to `/rp2040-matrix-setup`.

## 2. Find out what state the board is in

Run these checks:

```bash
ls /Volumes/RPI-RP2
mpremote connect list
mpremote exec "import sys; print(sys.version)"
```

The `ls` fails whenever the board is not in firmware mode. That is normal and not an error. Then read the results:

| Result | Meaning | Next |
|---|---|---|
| `/Volumes/RPI-RP2` exists | The board is in firmware mode | Go to step 3 |
| A MicroPython version is printed | The board is ready | Go to step 4 |
| `connect list` shows a `usbmodem` device, but `mpremote exec` says "no device found" | Your command sandbox is blocking the serial port, so the board is fine | Ask for permission to run the command outside the sandbox and repeat it. Do not blame the cable |
| No drive and no `usbmodem` device | The board is not connected, the cable carries no data, or the board runs other firmware without USB | Ask the user to reconnect it with a data cable, try another port and repeat the checks. If there is still nothing, ask them to hold BOOT while plugging in, then go to step 3 |

If the user explicitly asks to reinstall or upgrade the firmware, go to step 3 even when MicroPython answers.

## 3. Install the firmware (rare)

This is for a brand-new board, a board without MicroPython, or an upgrade the user asked for. Before flashing, explain that it replaces MicroPython and may erase files stored on the board. Files from this repository come back with step 4, but anything else on the board would be lost. Get an explicit yes first.

1. Ask the user to put the board in firmware mode: unplug the USB cable, hold the BOOT button, plug the cable in, then release BOOT. Wait for their confirmation, then check `ls /Volumes/RPI-RP2`. If the drive does not appear, try another cable or port, and make sure BOOT is held while plugging in.
2. Run `./deploy.sh --firmware`. It copies the `.uf2` file from `firmware/` to the board, waits up to ten seconds for the board to restart and lists its files. macOS may show a "disk not ejected properly" notice, which can be ignored.
3. If the script says the board did not come back, wait a few seconds and repeat the MicroPython check from step 2. If it still does not answer, ask the user to unplug and replug the board.
4. Continue with step 4.

## 4. Deploy the apps

Run `./deploy.sh --apps`. It copies `launcher.py` as `main.py`, then `lib/` and `apps/`, resets the saved app so the board starts on the first one, prints the file lists and restarts the board. The script prints every command it runs. Summarise the result and ignore the "File exists" lines from `mkdir`, which are harmless.

If a command fails to reach the board in the sandbox, ask for permission to run it outside the sandbox and repeat it.

## 5. Verify

- Compare `mpremote fs ls :apps` with `ls apps/*.py` and report any app missing on the board.
- The script copies files but never deletes them. A file on the board with no match in `apps/` or `lib/`, for example an app that was renamed or removed, is stale. List such files and offer to remove them with `mpremote fs rm :apps/<name>.py`. Ask before removing anything.
- Check that every name in the `APPS` list in `launcher.py` has a file in `apps/`.
- Ask the user to look at the board. The first app should be running, and BOOT should step to the next one.

## Jump to a specific app

After a deploy the board starts on the first app. To go straight to another one, for example a newly added app, read the `APPS` list in `launcher.py`, count the app's position from 0 and run the following with that number in place of `7`:

```bash
mpremote exec "open('app_index','w').write('7')"
mpremote reset
```

The board then starts on that app until the next deploy.

## Rules

- Never run `./deploy.sh --firmware` without an explicit yes from the user and without `/Volumes/RPI-RP2` present.
- Never delete files from the board without asking.
- Do not run `mpremote repl`. It keeps the USB port busy and blocks later commands. If a command reports a busy port, ask the user to close other serial programs such as Thonny, a serial monitor or another mpremote session.
- If the board shows nothing after a deploy, ask the user to press RESET. If it stays dark, suggest running `/rp2040-matrix-setup` again.
- To upgrade MicroPython, replace the `.uf2` file in `firmware/` and update `FIRMWARE_FILE` at the top of `deploy.sh`.
