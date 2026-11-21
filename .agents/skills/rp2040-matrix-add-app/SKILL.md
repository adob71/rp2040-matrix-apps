---
name: rp2040-matrix-add-app
description: >-
  Adds a new app to the RP2040-Matrix apps repository from the user's description.
  Writes apps/<app-name>.py with the ws2812 and touch libraries, registers it in
  launcher.py in alphabetical order, adds it to tools/make_preview.py, tests it by
  running it on the computer, creates its preview GIF and adds its row to the
  README. Use whenever the user wants to add, create, write, make or build an app,
  animation, game or LED pattern for the board, or to change an existing app, for
  example "make an app that shows a traffic light", even when they do not mention
  the repository structure. It never touches the board. Use rp2040-matrix-deploy to put
  the app on the board.
compatibility: Needs Python 3 and the .venv with Pillow created by rp2040-matrix-setup. Does not need the board.
---

# Add an app to the RP2040-Matrix

The goal is to create a new RP2040-Matrix app, generate its local GIF preview and update the app
list and README.

Keep the implementation simple and follow the steps in order. Stop at the first failure unless a
step says to continue. Run commands yourself and ask before installing software. Do not connect to,
reset or modify the board from this skill.

This skill is for macOS only. Do not attempt Linux, Windows or WSL setup.

If a command fails because your command sandbox blocks the network, USB access or files outside the
repository, ask permission to run it outside the sandbox and repeat it. Escalate only that one
command.

Placeholders in angle brackets, such as `<app-name>`, stand for real values. Write them without the
angle brackets.

## 1. Understand the request

The description can be one line ("a traffic light") or a detailed spec. Work out what the app shows,
its colors, its timing and whether it reacts to touch. Ask only when an answer would change the app
and cannot be assumed sensibly, with at most two questions in one message. Otherwise choose sensible
defaults, say what you assumed in a line or two and carry on. Don't ask about things that are easy
to change later, such as exact colors or speed.

If the user wants to change an existing app, skip steps 2 and 4, edit `apps/<app-name>.py` in
place and redo step 5. Redo step 6 only if the app's description changed.

## 2. Choose the name

Pick one short lowercase name made of letters, digits and underscores that starts with a letter,
such as `traffic`. Name what you see on the board: singular when one thing is shown at a time
(`heart`), plural when several are (`eyes`). The name must follow rule 8 of the app guide. Run
`ls apps/` first. Tell the user which name you chose.

## 3. Write the app

Read `references/app-guide.md`, then the existing app closest to the request: `apps/identicon.py` or
`apps/eyes.py` for fixed frames, `apps/emoji.py` for touch, `apps/dice.py` for touch with timing,
`apps/rain.py` or `apps/life.py` for computed frames. Write `apps/<app-name>.py` in the same style,
with settings in capitals at the top, short comments and no leftover debug output. The app must show
something immediately and its main loop must sleep.

## 4. Register the app

- Check that the `APPS` list in `launcher.py` is already in alphabetical order. If it is not, tell
  the user and ask where to insert the name. Otherwise add it in alphabetical position. This list is
  also the order in which the BOOT button steps through the apps, and the first entry is the app
  that runs after a deploy.
- In `tools/make_preview.py`, add one entry to the `APPS` dictionary (a different object from the
  list above) with `ms` for one full cycle of the animation, plus `taps` or `seed` when the app needs
  them. The guide explains how to choose.

## 5. Test it on the computer

The preview generator requires Pillow in `.venv`.

Check that the virtual environment exists and Pillow is available:

```bash
.venv/bin/python -c "from PIL import Image, ImageChops, ImageDraw, ImageFilter" \
  && echo "Pillow OK" \
  || echo "Pillow or .venv missing"
```

If it says missing, stop and run step 6 of the `rp2040-matrix-setup` skill.

Generate the preview:

```bash
perl -e 'alarm 20; exec @ARGV' .venv/bin/python tools/make_preview.py <app-name>
```

The tool runs the app with stand-in libraries and writes `preview/<app-name>.gif`.

- If generation fails, inspect the error and fix the actual cause. It may be an app, preview-tool or
  environment issue.
- Check `app-guide.md` if the app uses unsupported calls such as `machine`, `time.sleep_us` or
  `pad.touched`.
- If the command is killed after 20 seconds (exit status 142), the app's main loop probably never
  sleeps.
- Check that the output reports multiple frames and a duration close to `ms`. Identical consecutive
  frames may be merged.

Open the GIF so the user can see it:

```bash
open "preview/<app-name>.gif"
```

If `open` fails, ask permission to run it outside the sandbox. If it still fails, give the user the
full path (`$PWD/preview/<app-name>.gif`) to open themselves.

Do not substitute internal image inspection for opening the preview. Wait for the user to confirm
whether it matches what they pictured. Adjust until they are happy.

## 6. Add the README row

Add one row to the table under `## Apps` in `README.md`, at the alphabetical position:

```markdown
| traffic | Red, green and yellow lights in turn | ![traffic](preview/traffic.gif) |
```

The description is short, starts with a capital letter, has no full stop and uses "Touch to ..." for
apps that react to touch.

## 7. Report and hand over

Summarise the files actually changed. State the app's position in the `APPS` list counting from 0, after your final edit, and say if it
changed which app is first. Offer to
put it on the board with `rp2040-matrix-deploy`. Do not deploy or commit unless the user asks.

## Rules

- Do not edit `lib/`, `deploy.sh` or other apps to add an app. If the idea needs something the
  libraries cannot do, say so and ask before changing them.
- Never run deploy commands or touch the board in this skill.
- Keep the app in one file and keep it readable, because other people will copy it as an example.
