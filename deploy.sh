#!/bin/sh

FIRMWARE_FILE="firmware/RPI_PICO-20250911-v1.26.1.uf2"
BOOT_VOLUME="/Volumes/RPI-RP2"

usage() {
    echo "Usage: $0 [--firmware] [--apps]"
    echo "  --firmware   flash MicroPython (board must be in BOOTSEL mode)"
    echo "  --apps       copy launcher, lib and apps, then reset the board"
    exit 1
}

firmware() {
    if [ ! -d "$BOOT_VOLUME" ]; then
        echo "Board is not in BOOTSEL mode ($BOOT_VOLUME not found)."
        echo "Unplug it, hold the BOOTSEL button, plug it in again, then re-run."
        exit 1
    fi

    cp "$FIRMWARE_FILE" "$BOOT_VOLUME/" || {
        echo "Could not copy the firmware to $BOOT_VOLUME."
        exit 1
    }

    # the board reboots by itself after the copy: wait until mpremote can talk to it
    echo "Waiting for the board to restart..."
    for i in 1 2 3 4 5 6 7 8 9 10; do
        sleep 1
        if mpremote exec "pass" >/dev/null 2>&1; then
            mpremote fs ls || exit 1
            echo
            return
        fi
    done
    echo "The board did not come back after flashing."
    exit 1
}

apps() {
    mpremote exec "pass" >/dev/null 2>&1 || {
        echo "No board found over USB. Connect it, or run --firmware if it has no MicroPython."
        exit 1
    }

    mpremote fs cp launcher.py :main.py || exit 1

    mpremote exec "open('app_index','w').write('0')" || exit 1

    mpremote fs mkdir :lib || mpremote fs ls :lib >/dev/null || exit 1
    mpremote fs cp lib/*.py :lib/ || exit 1

    mpremote fs mkdir :apps || mpremote fs ls :apps >/dev/null || exit 1
    mpremote fs cp apps/*.py :apps/ || exit 1

    mpremote fs ls || exit 1
    echo

    mpremote fs ls :lib || exit 1
    echo

    mpremote fs ls :apps || exit 1
    echo

    mpremote reset || exit 1
}

# ---- main ----
DO_FIRMWARE=0
DO_APPS=0

if [ $# -eq 0 ]; then
    usage
fi

for arg in "$@"; do
    case "$arg" in
        --firmware|-f) DO_FIRMWARE=1 ;;
        --apps|-a)     DO_APPS=1 ;;
        *)             usage ;;
    esac
done

set -x

if [ "$DO_FIRMWARE" = 1 ]; then
    firmware
fi

if [ "$DO_APPS" = 1 ]; then
    apps
fi

set +x
