# RP2040-Matrix Apps

**Little apps for a little 5×5 LED computer**

Plug it into a USB port and it starts by itself.

This project runs on the [Waveshare RP2040-Matrix](https://www.waveshare.com/rp2040-matrix.htm), a development board by Waveshare built around the [Raspberry Pi RP2040](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf) microcontroller.

## The board

| RP2040-Matrix |
|---|
| <img src="docs/rp2040-matrix.png" width="500" alt="RP2040-Matrix, front and back"> |

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
| Touch pads (GP8–GP14) | Touch pads inside the yellow outline to control apps that react to touch. |
| BOOT button | Press to switch to the next app; after the last one it starts over. |
| RESET button | Press to restart the board; it comes back on the same app. |

## Apps

Press BOOT to step through the apps in this order.

| Name | Description | Preview |
|---|---|---|
| avatar | Little patterns like GitHub avatars | ![avatar](gifs/avatar.gif) |
| count | Counts 0 to 9 | ![count](gifs/count.gif) |
| dice | Touch to roll, touch again to stop | ![dice](gifs/dice.gif) |
| emoji | Touch to change the face | ![emoji](gifs/emoji.gif) |
| eyes | A face that raises its eyebrows | ![eyes](gifs/eyes.gif) |
| flag | Touch to raise the red flag | ![flag](gifs/flag.gif) |
| heart | A beating heart | ![heart](gifs/heart.gif) |
| life | Conway's Game of Life, a new random start each time | ![life](gifs/life.gif) |
| name | Spells a name in random colours | ![name](gifs/name.gif) |
| rain | Falling green digital rain | ![rain](gifs/rain.gif) |
| stars | Twinkling stars | ![stars](gifs/stars.gif) |

## Developers

1. Install mpremote: `brew install mpremote` (or `pip install mpremote`).
2. Clone the repo: `git clone https://github.com/adob71/rp2040-matrix-apps.git && cd rp2040-matrix-apps`
3. Add your app to `apps/`. For a first try, copy `apps/name.py` to `apps/hello.py` and change `TEXT`.
4. Add `"hello"` to the `APPS` list in `launcher.py`, keeping it in alphabetical order.
5. Connect the board by USB and run `./deploy.sh --apps`, then press BOOT until your app shows up. On a brand-new board, run `./deploy.sh --firmware` first.

More for developers is coming soon: the repo structure, the shared library, developing and deploying your own apps.

## License

MIT. See [LICENSE](LICENSE).

Waveshare and Raspberry Pi are trademarks of their respective owners. This is an independent project, not affiliated with or endorsed by either company.
