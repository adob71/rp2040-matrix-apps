# RP2040-Matrix Apps

Little apps for a little LED matrix computer

Plug it in and it runs.

This project runs on the [Waveshare RP2040-Matrix](https://www.waveshare.com/rp2040-matrix.htm), a development board built around the [Raspberry Pi RP2040](https://www.raspberrypi.com/products/rp2040/) microcontroller.

## Development Board

| Front | Back |
|:---:|:---:|
| <img src="docs/rp2040-matrix-front.png" width="300"> | <img src="docs/rp2040-matrix-back.png" width="300"> |

| # | Description |
|---|---|
| 1 | USB Type-C connector |
| 2 | 5×5 RGB LED matrix |
| 3 | Touch pads (GP8–GP14) |
| 4 | BOOT button |
| 5 | RESET button |
| 6 | RP2040 dual-core processor |

## Controls

| Control | Description |
|---|---|
| Touch pads (GP8–GP14) | Touch the pads inside the yellow outline to control apps that react to touch. |
| BOOT button | Press to switch to the next app; after the last one it starts over. |
| RESET button | Press to restart the board; it starts again on the same app. |

## Apps

Press BOOT to step through the apps in this order.

| Name | Description | Preview | Demo |
|---|---|---|---|
| clock | Analog clock with hour and minute hands | <img src="preview/clock.gif" width="100"> | [▶️](demo/clock.gif) |
| dice | Touch to roll a die, touch again to stop | <img src="preview/dice.gif" width="100"> | |
| emoji | Touch to cycle through emoji faces | <img src="preview/emoji.gif" width="100"> | |
| eyes | Animated eyes that raise their eyebrows | <img src="preview/eyes.gif" width="100"> | |
| flag | Touch to raise and lower the red flag | <img src="preview/flag.gif" width="100"> | |
| heart | Beating heart animation | <img src="preview/heart.gif" width="100"> | [▶️](demo/heart.gif) |
| identicon | Touch to cycle through identicons | <img src="preview/identicon.gif" width="100"> | |
| life | Game of Life from a random start | <img src="preview/life.gif" width="100"> | |
| name | Spells a custom name in random colors | <img src="preview/name.gif" width="100"> | [▶️](demo/name.gif) |
| rain | Falling green digital rain, Matrix-style | <img src="preview/rain.gif" width="100"> | [▶️](demo/rain.gif) |

## Developers

This repo is built to be used with an AI coding agent that supports [Agent Skills](https://agentskills.io). The skills have been tested using GitHub Copilot CLI, OpenAI Codex CLI and Cursor Agent CLI.

You also need a Mac, an RP2040-Matrix board and a USB Type-C data cable.

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

The [RP2040 datasheet](docs/rp2040-datasheet.pdf) is © Raspberry Pi Ltd, licensed under [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/) and included unmodified. The [RP2040-Matrix schematic](docs/rp2040-matrix-schematic.pdf) is published by Waveshare.
