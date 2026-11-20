import time
import random
import ws2812

STEP_MS = 300              # time between moves
END_MS = 1500              # pause before the next game
FLASH_COUNT = 3            # winning-line flashes
FLASH_MS = 200              # time for each on or off phase
X_COLOR = (255, 0, 0)      # (R, G, B)
O_COLOR = (0, 0, 255)

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winning_line(board, player):
    for a, b, c in WIN_LINES:
        if board[a] == player and board[b] == player and board[c] == player:
            return (a, b, c)
    return None


def has_won(board, player):
    return winning_line(board, player) is not None


def choose_move(board, player, opponent):
    empty = [i for i in range(9) if board[i] == 0]
    for mark in (player, opponent):
        for move in empty:
            board[move] = mark
            wins = has_won(board, mark)
            board[move] = 0
            if wins:
                return move
    return empty[random.randrange(len(empty))]


def draw(board, hidden=()):
    frame = [ws2812.OFF] * 25
    for cell in range(9):
        if board[cell] and cell not in hidden:
            row = 1 + cell // 3
            col = 1 + cell % 3
            color = X_COLOR if board[cell] == 1 else O_COLOR
            frame[row * 5 + col] = ws2812.pack(color[0], color[1], color[2])
    ws2812.show(frame)


while True:
    board = [0] * 9
    player = 1
    draw(board)
    while True:
        time.sleep_ms(STEP_MS)
        move = choose_move(board, player, 3 - player)
        board[move] = player
        draw(board)
        line = winning_line(board, player)
        if line is not None or all(board):
            break
        player = 3 - player
    if line is not None:
        for _ in range(FLASH_COUNT):
            draw(board, line)
            time.sleep_ms(FLASH_MS)
            draw(board)
            time.sleep_ms(FLASH_MS)
    time.sleep_ms(END_MS)
