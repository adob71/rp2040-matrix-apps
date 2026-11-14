# RP2040-Matrix Apps

**Little apps for a little 5×5 LED computer**

Plug it into a USB port and it starts by itself.

This project runs on the [Waveshare RP2040-Matrix](https://www.waveshare.com/rp2040-matrix.htm), a development board built around the [Raspberry Pi RP2040](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf) microcontroller.

## The board

| Front | Back |
|:---:|:---:|
| <img src="docs/rp2040-matrix-front.png" width="300" alt="RP2040-Matrix front"> | <img src="docs/rp2040-matrix-back.png" width="300" alt="RP2040-Matrix back"> |

| # | Description |
|---|---|
| 1 | USB Type-C connector |
| 2 | 5×5 RGB LED Matrix |
| 3 | Touch pads (GP8–GP14) |
| 4 | BOOT button |
| 5 | RESET button |
| 6 | RP2040 dual-core processor |

## Controls

| Control | Description |
|---|---|
| Touch pads (GP8–GP14) | Touch the pads inside the yellow outline to control apps that react to touch. |
| BOOT button | Press to switch to the next app; after the last one it starts over. |
| RESET button | Press to restart the board; it comes back on the same app. |

## Apps

Press BOOT to step through the apps in this order.

| Name | Description | Preview |
|---|---|---|
| avatar | Little patterns like GitHub avatars | <img src="gifs/avatar.gif" width="100" alt="avatar"> |
| clock | Red hour hand and blue minute hand | <img src="gifs/clock.gif" width="100" alt="clock"> |
| count | Counts 0 to 9 | <img src="gifs/count.gif" width="100" alt="count"> |
| dice | Touch to roll, touch again to stop | <img src="gifs/dice.gif" width="100" alt="dice"> |
| emoji | Touch to change the face | <img src="gifs/emoji.gif" width="100" alt="emoji"> |
| eyes | A face that raises its eyebrows | <img src="gifs/eyes.gif" width="100" alt="eyes"> |
| flag | Touch to raise the red flag | <img src="gifs/flag.gif" width="100" alt="flag"> |
| heart | A beating heart | <img src="gifs/heart.gif" width="100" alt="heart"> |
| life | Game of Life, a new random start each time | <img src="gifs/life.gif" width="100" alt="life"> |
| name | Spells a name in random colours | <img src="gifs/name.gif" width="100" alt="name"> |
| rain | Falling green digital rain | <img src="gifs/rain.gif" width="100" alt="rain"> |
| stars | Twinkling stars | <img src="gifs/stars.gif" width="100" alt="stars"> |

## Developers

This repo is built to be used with an AI coding agent that supports [Agent Skills](https://agentskills.io). The skills have been tested using GitHub Copilot CLI, OpenAI Codex CLI and Cursor Agent CLI.

You also need macOS, an RP2040-Matrix board and a USB Type-C data cable.

```bash
git clone https://github.com/adob71/rp2040-matrix-apps.git && cd rp2040-matrix-apps
```

Open your agent in the folder and ask for what you want. It picks the matching skill:

| Prompt | Skill |
|---|---|
| Set up my computer for this repo | `rp2040-matrix-setup` |
| Deploy to my board | `rp2040-matrix-deploy` |
| Add an app that shows a traffic light | `rp2040-matrix-add-app` |

No AI coding agent? The skills in `.agents/skills/` are plain step-by-step instructions you can follow by hand.

## License

MIT. See [LICENSE](LICENSE).

Waveshare and Raspberry Pi are trademarks of their respective owners. This is an independent project, not affiliated with or endorsed by either company.
