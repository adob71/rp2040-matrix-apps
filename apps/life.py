import time
import random
import ws2812

SIZE = 5
CELLS = SIZE * SIZE
STEP_MS = 300        # time per generation
FILL = 0.4           # chance that a cell is alive in a new random start
MIN_ALIVE = 4        # skip boring starts with fewer live cells than this
HISTORY = 12         # generations remembered to spot repeating patterns
MIN_STEPS = 12       # a repeating pattern runs at least this many generations before restart
MAX_STEPS = 60       # restart after this many generations (gliders take a long time to repeat)
END_MS = 1500        # pause on the final pattern before restarting

SURVIVOR = (0, 0, 255)       # (R, G, B) cell that was alive last generation too
NEWBORN = (255, 255, 255)    # (R, G, B) cell born this generation

PX_SURVIVOR = ws2812.pack(SURVIVOR[0], SURVIVOR[1], SURVIVOR[2])
PX_NEWBORN = ws2812.pack(NEWBORN[0], NEWBORN[1], NEWBORN[2])

def random_board():
    while True:
        board = [1 if random.random() < FILL else 0 for _ in range(CELLS)]
        if sum(board) >= MIN_ALIVE:
            return board

def step(board):
    # edges wrap around (torus), so a glider that leaves one side comes back on the other
    new = [0] * CELLS
    for r in range(SIZE):
        for c in range(SIZE):
            n = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        n += board[((r + dr) % SIZE) * SIZE + (c + dc) % SIZE]
            alive = board[r * SIZE + c]
            new[r * SIZE + c] = 1 if n == 3 or (alive and n == 2) else 0
    return new

def draw(board, prev):
    frame = []
    for i in range(CELLS):
        if board[i]:
            frame.append(PX_SURVIVOR if prev[i] else PX_NEWBORN)
        else:
            frame.append(ws2812.OFF)
    ws2812.show(frame)

while True:
    board = random_board()
    prev = [0] * CELLS            # everything shows as newborn on the first frame
    seen = []
    steps = 0
    draw(board, prev)
    time.sleep_ms(STEP_MS)
    while True:
        if not any(board) or steps >= MAX_STEPS:
            break                 # everything died, or it has run long enough
        key = bytes(board)
        if key in seen and steps >= MIN_STEPS:
            break                 # settled into a still life or a repeating cycle
        seen.append(key)
        if len(seen) > HISTORY:
            seen.pop(0)
        prev, board = board, step(board)
        steps += 1
        draw(board, prev)
        time.sleep_ms(STEP_MS)
    time.sleep_ms(END_MS)
