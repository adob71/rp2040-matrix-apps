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

The goal is a working macOS development environment ready for `/rp2040-matrix-deploy`
and `/rp2040-matrix-add-app`.

Keep the setup simple and follow the steps in order. Stop at the first failure.
Run commands yourself and ask before installing software or interrupting a
running application.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

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

## 3. Install mpremote

Check:

```bash
brew list --versions mpremote
command -v mpremote
mpremote --version
```

On Apple Silicon, the expected executable is /opt/homebrew/bin/mpremote, installed and managed by Homebrew.

If Homebrew does not have mpremote installed, ask the user for permission and install:

```bash
brew install mpremote
```

If mpremote exists but is not the Homebrew version, explain the conflict and ask before changing or uninstalling anything. Do not use pip or pipx.

Verify:

```bash
brew list --versions mpremote
command -v mpremote
mpremote --version
test "$(command -v mpremote)" = "$(brew --prefix)/bin/mpremote"
```

## 4. Find the board

Run these checks:

```bash
if [ -d /Volumes/RPI-RP2 ]; then
    echo "RP2040 BOOTSEL mass-storage mode detected"
else
    echo "RP2040 firmware volume not detected"
    mpremote connect list
fi
```

If /Volumes/RPI-RP2 exists, the board is in BOOTSEL mass-storage mode. Do not continue with serial detection or MicroPython verification. Stop here and continue with /rp2040-matrix-deploy to install or update MicroPython firmware.

A board running MicroPython should appear as a USB serial device,
typically `/dev/cu.usbmodem101` on macOS.

If no device appears:
- Check that the board is connected.
- Make sure the USB cable supports data.
- Try another USB port.
- Retry the command.

If multiple devices appear, ask the user to disconnect other serial
devices so the correct board can be identified.

## 5. Verify MicroPython

Before running mpremote exec, explain that it may soft-reset the board and interrupt the running application. Ask permission every time before running it.

Run:

Use the actual USB serial port identified in Step 4. Do not assume a fixed port name.

For example, if the detected port is `/dev/cu.usbmodem101`:

```bash
mpremote connect /dev/cu.usbmodem101 exec "import sys; print(sys.version)"
```

The output must identify MicroPython and show its version.

If the port is busy, ask the user to close other serial applications
such as Thonny, a serial monitor or another mpremote session.

If there is no response, ask the user to press RESET and retry once.

If `mpremote connect list` showed the board but `mpremote exec` says "no device found", your command sandbox is blocking the serial port. Ask for permission to run it outside the sandbox and repeat it before suggesting a cable problem.

## 6. Set up preview tooling

The preview tool runs applications on the Mac and generates GIF previews without requiring the physical board.

Check whether the repository-local virtual environment exists and Pillow is available:

```bash
if [ -x .venv/bin/python ]; then
    .venv/bin/python -c "import PIL; print(PIL.__version__)"
else
    echo "Preview environment not ready"
fi
```

If the environment or Pillow is missing, ask permission before creating the virtual environment or installing dependencies.

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
- Board: detected or not detected, show USB port
- MicroPython: verified with version, not verified, or unavailable
- Preview tooling: ready or not installed

Next steps:

1. `/rp2040-matrix-deploy` — install firmware if needed and deploy the apps.
2. `/rp2040-matrix-add-app <description>` — create a new application.