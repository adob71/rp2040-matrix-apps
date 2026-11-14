---
name: rp2040-matrix-setup
description: >-
  One-time setup of the macOS development environment for the RP2040-Matrix
  apps repository. Installs mpremote using Homebrew, checks the repository,
  finds the board over USB and verifies that MicroPython responds.
  Use when a user is new to the repository, asks to set up or get started,
  install mpremote, connect the board, or reports "board not found" or
  mpremote errors. Run once per computer.
compatibility: macOS, Homebrew, Python 3 and an RP2040-Matrix board connected over USB.
---

# Set up the RP2040-Matrix development environment

The goal is a working macOS development environment ready for `/rp2040-matrix-deploy` and
`/rp2040-matrix-add-app`.

Keep the setup simple and follow the steps in order. Stop at the first failure unless a step says to
continue. Run commands yourself and ask before installing software or interrupting a running
application.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

If a command fails because your command sandbox blocks the network, USB access or files outside the
repository, ask permission to run it outside the sandbox and repeat it.

## 1. Check the repository

Check that the current directory contains:

- `launcher.py`
- `deploy.sh`
- `apps/`
- `lib/`

If the repository is missing, ask the user before cloning:

```bash
git clone https://github.com/adob71/rp2040-matrix-apps.git
cd rp2040-matrix-apps
```

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

- Homebrew does not have mpremote and no other copy exists: ask for permission, then run `brew
  install mpremote`.
- Another copy comes first in the `which -a` list, for example under `~/.local/bin` from pip or
  pipx: explain the conflict and show both paths. Ask before changing anything. If the user agrees
  to remove the other copy, use the tool that installed it, such as `pipx uninstall mpremote` or
  `python3 -m pip uninstall mpremote`.

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
    echo "RP2040 firmware volume not detected"
    mpremote connect list
fi
```

`mpremote connect list` always shows two built-in macOS entries, `/dev/cu.Bluetooth-Incoming-Port`
and `/dev/cu.debug-console`. Ignore them. Only a `usbmodem` device is the board.

- `/Volumes/RPI-RP2` exists: the board is in firmware/BOOTSEL mode. Skip step 5 because nothing
  answers over serial yet, continue with step 6, and report in step 7 that MicroPython is not
  installed yet and that `/rp2040-matrix-deploy` installs it.
- A `usbmodem` device is listed: this is the board. Continue with step 5.
- No `usbmodem` device and no `RPI-RP2` drive: check that the board is connected, that the USB cable
  carries data, and try another port, then run the command again. If there is still nothing, ask the
  user to hold BOOT while plugging the board in, which puts it in firmware mode.
- More than one `usbmodem` device: ask which one is the board, and ask the user to unplug the
  others.

## 5. Verify MicroPython

Before running `mpremote exec`, explain that it may soft-reset the board and interrupt the running
application. Ask permission every time before running it.

Use the actual USB serial port identified in step 4. Do not assume a fixed port name.

For example, if the detected port is `/dev/cu.usbmodem101`:

```bash
mpremote connect /dev/cu.usbmodem101 exec "import sys; print(sys.version)"
```

The output must identify MicroPython and show its version.

If the command says "no device found", "failed to access" or that the port is busy, your command
sandbox is probably blocking the serial port, because the board was just listed:
1. Ask permission to retry the same command outside the command sandbox.
2. If it still fails, ask the user to run `lsof /dev/cu.usbmodem101` in macOS Terminal. Replace the
   example port with the actual detected port.
3. If `lsof` returns no process, ask the user to retry the version check directly in Terminal.
4. If a process is identified, ask the user to close the corresponding application before retrying.

If the board stops responding during the check, ask the user to press RESET and retry once.

Do not report MicroPython as verified unless the version check succeeds.

## 6. Set up preview tooling

The preview tool runs applications on the Mac and generates GIF previews without requiring the
physical board.

Check whether the repository-local virtual environment exists and Pillow is available:

```bash
if [ -x .venv/bin/python ]; then
    .venv/bin/python -c "import PIL; print(PIL.__version__)"
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
.venv/bin/python -c "import PIL; print(PIL.__version__)"
```

Do not install Pillow globally or use Homebrew for this dependency.

## 7. Report

Give a short summary of the actual results:

- Repository: ready or missing
- Homebrew: available or missing
- mpremote: installed, show version and executable path
- Board: detected (show the USB port), in firmware mode, or not detected
- MicroPython: verified with version, not installed yet, not verified, or unavailable
- Preview tooling: ready or not installed

Next steps:

1. `/rp2040-matrix-deploy` — install firmware if needed and deploy the apps.
2. `/rp2040-matrix-add-app <description>` — create a new application.
