import time
import random
import ws2812

SIZE = 5
CELLS = SIZE * SIZE
STEP_MS = 300        # time per generation
FILL = 0.4           # chance that a cell is alive in a new random start
MIN_ALIVE = 4        # skip boring starts with fewer live cells than this
HISTORY = 12         # generations remembered to spot repeating patterns
STIR = 3             # live cells added when the pattern settles
MAX_GENS = 150       # reseed after this many generations (about 45 s at 300 ms)

ALIVE = ws2812.pack(0, 0, 255)

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

def stir(board):
    # bring a few dead cells to life so the pattern never settles for good
    dead = [i for i in range(CELLS) if not board[i]]
    for _ in range(min(STIR, len(dead))):
        board[dead.pop(random.randrange(len(dead)))] = 1
    return board

def draw(board):
    ws2812.show([ALIVE if cell else ws2812.OFF for cell in board])

board = random_board()
seen = []
gens = 0
while True:
    draw(board)
    time.sleep_ms(STEP_MS)
    seen.append(bytes(board))
    if len(seen) > HISTORY:
        seen.pop(0)
    board = step(board)
    gens += 1
    if gens >= MAX_GENS or not any(board):
        board = random_board()      # everything died, or it ran long enough
        seen = []
        gens = 0
    elif bytes(board) in seen:
        board = stir(board)         # settled into a still life or short cycle
        seen = []
