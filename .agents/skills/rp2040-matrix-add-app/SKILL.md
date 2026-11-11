---
name: rp2040-matrix-add-app
description: >-
  Adds a new app to the RP2040-Matrix apps repository from the user's description.
  Writes apps/<name>.py with the ws2812 and touch libraries, registers it in
  launcher.py in alphabetical order, adds it to tools/make_gif.py, tests it by
  running it on the computer, creates its preview GIF and adds its row to the
  README. Use whenever the user wants to add, create, write, make or build an app,
  animation, game or LED pattern for the board, or to change an existing app, for
  example "make an app that shows a traffic light", even when they do not mention
  the repository structure. It never touches the board. Use rp2040-matrix-deploy to put
  the app on the board.
compatibility: Needs Python 3 and the .venv with Pillow created by rp2040-matrix-setup. Does not need the board.
---

# Add an app to the RP2040-Matrix

The goal is to create a new RP2040-Matrix app, generate its local GIF preview
and update the app list and README.

Keep the implementation simple and follow the steps in order. Stop at the first
failure unless a step says to continue. Run commands yourself and ask before
installing software. Do not connect to, reset or modify the board from this skill.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

If a command fails because your command sandbox blocks the network, USB access
or files outside the repository, ask permission to run it outside the sandbox
and repeat it.

## 1. Understand the request

The description can be one line ("a traffic light") or a detailed spec. Work out what the app shows, its colours, its timing and whether it reacts to touch. Ask only when an answer would change the app and cannot be assumed sensibly, with at most two questions in one message. Otherwise choose sensible defaults, say what you assumed in a line or two and carry on. Don't ask about things that are easy to change later, such as exact colours or speed.

If the user wants to change an existing app, edit that file in place and then redo steps 5 and 6 for it.

## 2. Choose the name

Pick one short lowercase word that is a valid Python name, such as `traffic`. Name what you see on the board: singular when one thing is shown at a time (`heart`), plural when several are (`stars`). The name must not match a file in `apps/` or a module name such as `time`, `math`, `random`, `touch` or `ws2812`, because the launcher imports apps by name. Tell the user which name you chose.

## 3. Write the app

Read `references/app-guide.md`, then the existing app closest to the request: `apps/avatar.py` or `apps/eyes.py` for fixed frames, `apps/emoji.py` for touch, `apps/dice.py` for touch with timing, `apps/stars.py` or `apps/life.py` for computed frames. Write `apps/<name>.py` in the same style, with settings in capitals at the top, short comments and no leftover debug output. The app must show something immediately and its main loop must sleep.

## 4. Register the app

- Add the name to the `APPS` list in `launcher.py`, keeping the list in alphabetical order. This list is also the order in which the BOOT button steps through the apps.
- Add an entry to the `APPS` table in `tools/make_gif.py` with `ms` for one full cycle of the animation, plus `taps` or `seed` when the app needs them. The guide explains how to choose.

## 5. Test it on the computer

Run `.venv/bin/python tools/make_gif.py <name>`. If `.venv` does not exist, tell the user to run `rp2040-matrix-setup` and stop here. The tool runs the app with stand-in libraries and writes `gifs/<name>.gif`.

- A traceback is a bug in the app. Fix it and run again.
- An `AttributeError` or `ModuleNotFoundError` means the app uses something the preview does not support, such as `machine`, `time.sleep_us` or `pad.touched`. Switch to a supported call (see the guide) before touching the tool.
- If the command is still running after about 20 seconds, stop it. The main loop never sleeps, so the fake clock never advances.
- Read the output line. An animation should show more than one frame, and the total time should be close to `ms`. A single frame from an animation usually means the loop never changes what it shows.

Then ask the user to look at the result with `open gifs/<name>.gif` and say whether it matches what they pictured. Adjust until they are happy.

## 6. Add the README row

Add one row to the table under `## Apps` in `README.md`, at the alphabetical position:

```markdown
| traffic | Red, green and yellow lights in turn | ![traffic](gifs/traffic.gif) |
```

The description is short, starts with a capital letter, has no full stop and uses "Touch to ..." for apps that react to touch.

## 7. Report and hand over

Summarise the changed files: `apps/<name>.py`, `launcher.py`, `tools/make_gif.py`, `gifs/<name>.gif` and `README.md`. State the app's position in `APPS` counting from 0. Offer to put it on the board with `rp2040-matrix-deploy`, which can jump straight to it. Do not deploy and do not commit unless the user asks.

## Rules

- Do not edit `lib/`, `deploy.sh` or other apps to add an app. If the idea needs something the libraries cannot do, say so and ask before changing them.
- Never run deploy commands or touch the board in this skill.
- Keep the app in one file and keep it readable, because other people will copy it as an example.
