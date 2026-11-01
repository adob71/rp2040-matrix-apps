---
name: rp2040-setup
description: >-
  One-time setup of the macOS development environment for the RP2040-Matrix
  apps repository. Installs mpremote using Homebrew, checks the repository,
  finds the board over USB and verifies that MicroPython responds.
  Use when a user is new to the repository or asks to set up the environment.
  Run once per computer.
compatibility: macOS, Homebrew, Python 3 and an RP2040-Matrix board connected over USB.
---

# Set up the RP2040-Matrix development environment

The goal is a working macOS development environment ready for `/rp2040-deploy`
and `/rp2040-add-app`.

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
```

If Homebrew is missing, stop and explain that Homebrew is required.

## 3. Install mpremote

Check:

```bash
command -v mpremote
```

If missing, ask the user for permission and install:

```bash
brew install mpremote
```

Verify:

```bash
mpremote --version
```

## 4. Find the board

Run:

```bash
mpremote connect list
```

A board running MicroPython should appear as a USB serial device,
typically `/dev/cu.usbmodem101` on macOS.

If no device appears:
- Check that the board is connected.
- Make sure the USB cable supports data.
- Try another USB port.
- Retry the command.

If `/Volumes/RPI-RP2` exists, the board is in firmware mode.
Stop here and continue with `/rp2040-deploy`.

If multiple devices appear, ask the user to disconnect other serial
devices so the correct board can be identified.

## 5. Verify MicroPython

Before executing anything on the board, explain that connecting or
executing commands may interrupt the running application.

Ask permission if necessary.

Run:

```bash
mpremote exec "import sys; print(sys.version)"
```

The output must identify MicroPython and show its version.

If the port is busy, ask the user to close other serial applications
such as Thonny, a serial monitor or another mpremote session.

If there is no response, ask the user to press RESET and retry once.

## 6. Set up preview tooling

The preview tool runs applications on the Mac and generates GIF previews
without requiring the physical board.

Check whether Pillow is already available.

If not, ask permission before creating the virtual environment
or installing dependencies.

```bash
python3 -m venv .venv
.venv/bin/pip install pillow
```

Verify:

```bash
.venv/bin/python -c "import PIL; print(PIL.__version__)"
```

## 7. Report

Give a short summary:

- Repository: ready
- mpremote: installed, show path
- Board: detected, show USB port and MicroPython version
- Preview tooling: ready or not installed

Next steps:

1. `/rp2040-deploy` — install firmware if needed and deploy the apps.
2. `/rp2040-add-app <description>` — create a new application.