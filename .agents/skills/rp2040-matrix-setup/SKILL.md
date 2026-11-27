---
name: rp2040-matrix-setup
description: >-
  One-time setup of the macOS development environment for the RP2040-Matrix
  apps repository. Installs mpremote using Homebrew, checks the repository,
  finds the board over USB and verifies that MicroPython responds.
  Use when a user is new to the repository, asks to set up or get started,
  install mpremote, connect the board, or reports "board not found" or
  mpremote errors. Run once per computer, and again in each new clone for the preview environment.
compatibility: macOS, Homebrew, Python 3 and an RP2040-Matrix board connected over USB.
---

# Set up the RP2040-Matrix development environment

The goal is a working macOS development environment ready for the `rp2040-matrix-deploy` and
`rp2040-matrix-add-app` skills.

Keep the setup simple and follow the steps in order. Stop at the first failure, except that a missing
board (step 4) or unverified MicroPython (step 5) must not stop step 6, because the preview tooling
needs no board. Run commands yourself and ask before installing software or interrupting a running
application.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

If a command fails because your command sandbox blocks the network, USB access or files outside the
repository, ask permission to run it outside the sandbox and repeat it. Escalate only that one
command.

Placeholders in angle brackets, such as `<app-name>`, stand for real values. Write them without the
angle brackets.

## 1. Check the repository

Check that the current directory contains `launcher.py`, `deploy.sh`, `apps/`, `lib/`,
`tools/make_preview.py` and `firmware/`.

If it does not, do not clone into the current directory. Ask the user where to put the repository,
then ask before running `git clone https://github.com/adob71/rp2040-matrix-apps.git` there. Use that
folder as the working directory for every later command; do not rely on `cd` persisting between
commands.

## 2. Check Homebrew

Run:

```bash
command -v brew
brew --version
```

If Homebrew is missing, stop and explain that Homebrew is required.

## 3. Install mpremote with Homebrew

In this project Homebrew manages mpremote. Never install it with pip or pipx.

Check:

```bash
brew list --versions mpremote 2>/dev/null || true
which -a mpremote 2>/dev/null || true
mpremote --version 2>/dev/null || true
```

Homebrew installs it in `$(brew --prefix)/bin`, which is `/opt/homebrew/bin` on Apple Silicon.

- Homebrew does not have mpremote and no other copy exists: ask for permission, then run
  `brew install mpremote`.
- Homebrew does not have mpremote but another copy exists (for example under `~/.local/bin`): show
  the path, explain that Homebrew manages mpremote in this project, ask before installing, then run
  `brew install mpremote`. Check again which copy comes first.
- Another copy comes first in the `which -a` list: show both paths and ask before changing anything.
  If the user agrees to remove it, first work out what installed it from its path or from
  `pipx list`. Use `pipx uninstall mpremote` for pipx. For pip, use the Python that owns that copy,
  with `-y`: `/path/to/that/python -m pip uninstall -y mpremote`. Never uninstall from the
  repository's `.venv`. If `$VIRTUAL_ENV` is set, tell the user that the virtual environment can
  shadow the Homebrew copy.

Verify:

```bash
brew list --versions mpremote
command -v mpremote
mpremote --version
test "$(command -v mpremote)" = "$(brew --prefix)/bin/mpremote"
```

## 4. Find the board

Run:

```bash
if [ -d /Volumes/RPI-RP2 ]; then
    echo "RP2040 BOOTSEL mass-storage mode detected"
else
    echo "RP2040 BOOTSEL volume not detected"
    mpremote connect list
fi
```

`mpremote connect list` always shows two built-in macOS entries, `/dev/cu.Bluetooth-Incoming-Port`
and `/dev/cu.debug-console`. Ignore them. Only a `usbmodem` device is the board.

- `/Volumes/RPI-RP2` exists: the board is in BOOTSEL mode. Skip step 5 because nothing answers over
  serial. Continue with step 6 and report in step 7 that MicroPython was not checked, because a
  board in BOOTSEL mode cannot be queried. The `rp2040-matrix-deploy` skill installs MicroPython if
  needed.
- A `usbmodem` device is listed: this is the board. Continue with step 5.
- No `usbmodem` device and no `RPI-RP2` drive: check that the board is connected, that the USB cable
  carries data, and try another port, then run the command again. If there is still nothing, ask the
  user to hold BOOT while plugging the board in, which puts it in BOOTSEL mode, then run the command again.
- More than one `usbmodem` device: ask which one is the board, and ask the user to unplug the
  others.

## 5. Verify MicroPython

Before running `mpremote exec`, explain that it may soft-reset the board and interrupt the running
application. Ask once, before the first `mpremote exec` of this session, and do not ask again for the same check.

Use the actual USB serial port identified in step 4. Do not assume a fixed port name.

For example, if the detected port is `/dev/cu.usbmodem101`:

```bash
mpremote connect /dev/cu.usbmodem101 exec "import sys; print(sys.version)" 2>&1 | tail -c 3000
```

The `tail` keeps the output short, because a board that runs a program printing nonstop (see below)
would flood it.

The output must identify MicroPython and show its version.

If the command says "no device found", "failed to access" or that the port is busy, your command
sandbox is probably blocking the serial port, because the board was just listed:
1. Ask permission to retry the same command outside the command sandbox.
2. If it still fails, ask the user to run `lsof /dev/cu.usbmodem101` in macOS Terminal. Replace the
   example port with the actual detected port.
3. If `lsof` returns no process, ask the user to retry the version check directly in Terminal.
4. If a process is identified, ask the user to close the corresponding application before retrying.

If the command fails with "could not enter raw repl", do not ask the user to press RESET. A board
straight from Waveshare runs a factory test (repeating "GPIO test" and "ADC test" lines) that blocks
the REPL, and RESET only restarts it. Report MicroPython as not verified (REPL blocked, probably the
factory test), tell the user to put the board in BOOTSEL mode by holding BOOT while plugging it in,
and continue with step 6. The `rp2040-matrix-deploy` skill then installs MicroPython.

For any other stall, ask the user to press RESET and retry once.

Do not report MicroPython as verified unless the version check succeeds.

## 6. Set up preview tooling

The preview tool runs applications on the Mac and generates GIF previews without requiring the
physical board.

Check whether the repository-local virtual environment exists and Pillow is available:

```bash
if [ -x .venv/bin/python ]; then
    .venv/bin/python -c "import PIL; from PIL import Image, ImageChops, ImageDraw, ImageFilter; print(PIL.__version__)"
else
    echo "Preview environment not ready"
fi
```

If the environment or Pillow is missing, ask permission before creating the virtual environment or
installing dependencies.

```bash
if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install pillow
```

Verify:

```bash
.venv/bin/python -c "import PIL; from PIL import Image, ImageChops, ImageDraw, ImageFilter; print(PIL.__version__)"
```

Do not install Pillow globally or use Homebrew for this dependency.

## 7. Report

Give a short summary of the actual results:

- Repository: ready or missing
- Homebrew: available or missing
- mpremote: installed, show version and executable path
- Board: detected (show the USB port), in BOOTSEL mode, not detected, or detected but blocking the
  REPL (probably the factory test)
- MicroPython: verified with version, not checked (BOOTSEL mode), not verified (REPL blocked),
  not verified (other reason), or unavailable
- Preview tooling: ready or not installed

Next steps:

1. The `rp2040-matrix-deploy` skill — install firmware if needed and deploy the apps.
2. The `rp2040-matrix-add-app` skill, with a description of the app — create a new application.
3. If the board blocks the REPL, hold BOOT while plugging it in, then use the
   `rp2040-matrix-deploy` skill. It installs MicroPython.
