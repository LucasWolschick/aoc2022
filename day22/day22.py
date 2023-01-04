import sys
import math
import string

WALL, EMPTY, BLOCKED = ["wall", "empty", "blocked"]
board = []
board_str, instructions_str, *_ = sys.stdin.read().split("\n\n")
for l in board_str.splitlines():
    if l.strip() == "":
        continue

    row = []
    for c in l.rstrip():
        if c == " ":
            row.append(WALL)
        elif c == ".":
            row.append(EMPTY)
        elif c == "#":
            row.append(BLOCKED)
    board.append(row)

width = max(len(r) for r in board)
height = len(board) 

instructions_str = instructions_str.strip()
instructions = []
i = 0
while i < len(instructions_str):
    ch = instructions_str[i]
    if ch == "R" or ch == "L":
        instructions.append(ch)
        i += 1
    else:
        start = i
        while i < len(instructions_str) and instructions_str[i] in string.digits:
            i += 1
        instructions.append(int(instructions_str[start:i]))

# find the first open space
def find_start(board):
    for y, l in enumerate(board):
        for x, c in enumerate(l):
            if c == EMPTY:
                return (x, y)
    return (0,0) 

def get(board, pos):
    x, y = pos
    if y < 0 or y >= len(board):
        return WALL
    elif x < 0 or x >= len(board[y]):
        return WALL
    else:
        return board[y][x]

def clamp(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x

def print_board(board, marker=None):
    rows = []

    for y, row in enumerate(board):
        s = []
        
        for x, col in enumerate(row):
            if (x, y) == marker:
                s.append("X")
            elif col == WALL:
                s.append(" ")
            elif col == EMPTY:
                s.append(".")
            elif col == BLOCKED:
                s.append("#")
        rows.append("".join(s))

    print("\n".join(rows))

orient = 0
pos = find_start(board)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for ins in instructions:
    if ins == "L":
        orient = (orient - 1) % 4
    elif ins == "R":
        orient = (orient + 1) % 4
    else:
        counter = ins
        while counter > 0:
            direction = DIRECTIONS[orient]
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            what = get(board, new_pos)
            if what == EMPTY:
                # move!
                pos = new_pos
            elif what == BLOCKED:
                # stop!
                break
            elif what == WALL:
                # wrap around!
                new_pos = (pos[0] - direction[0]*width, pos[1] - direction[1]*height)
                new_pos = (clamp(new_pos[0], 0, width-1), clamp(new_pos[1], 0, height-1))
                while get(board, new_pos) == WALL:
                    new_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])
                if get(board, new_pos) == EMPTY:
                    pos = new_pos
                else:
                    break
            counter -= 1
# part 1
ans1 = 1000*(pos[1] + 1) + 4*(pos[0] + 1) + orient
print(ans1)

# part 2
# attempt to build THE CUBE
L = 4 if ans1 == 6032 else 50 
if L == 4:
    exit()
    # don't attempt to solve the example

def get_cell(pos):
    norm = (pos[0] // L, pos[1] // L)
    match norm:
        case (1, 0): return 1
        case (2, 0): return 2
        case (1, 1): return 3
        case (0, 2): return 4
        case (1, 2): return 5
        case (0, 3): return 6

def cell_to_pos(cell):
    match cell:
        case 1: return (L, 0)
        case 2: return (2*L, 0)
        case 3: return (L, L)
        case 4: return (0, 2*L)
        case 5: return (L, 2*L)
        case 6: return (0, 3*L)
    assert False

orient = 0
pos = find_start(board)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
for ins in instructions:
    if ins == "L":
        orient = (orient - 1) % 4
    elif ins == "R":
        orient = (orient + 1) % 4
    else:
        counter = ins
        while counter > 0:
            direction = DIRECTIONS[orient]
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            what = get(board, new_pos)
            if what == EMPTY:
                # move!
                pos = new_pos
            elif what == BLOCKED:
                # stop!
                break
            elif what == WALL:
                # wrap around!
                cell = get_cell(pos)
                nopos = (pos[0] % L, pos[1] % L)
                match (orient, cell):
                    case (0, 2):
                        # 2-right
                        # emerge on right edge of 5 (flip 180)
                        c = cell_to_pos(5)
                        new_pos = (c[0] + L - 1, c[1] + L - nopos[1] - 1)
                        norient = 2
                    case (0, 3):
                        # 3-right
                        # emerge on bottom edge of 2 
                        c = cell_to_pos(2)
                        new_pos = (c[0] + nopos[0], c[1] + L - 1)
                        norient = 3
                    case (0, 5):
                        # 5-right
                        # emerge on right edge of 2
                        c = cell_to_pos(2)
                        new_pos = (c[0] + L - 1, c[1] + L - nopos[1] - 1)
                        norient = 2
                    case (0, 6):
                        # 6-right
                        # emerge on bottom edge of 5
                        c = cell_to_pos(5)
                        new_pos = (c[0] + nopos[1], c[1] + L - 1)
                        norient = 3
                    case (1, 2):
                        # 2-bot
                        # emerge on right edge of 3
                        c = cell_to_pos(3)
                        new_pos = (c[0] + L - 1, c[1] + nopos[0])
                        norient = 2
                    case (1, 5):
                        # 5-bot
                        # emerge on right edge of 6
                        c = cell_to_pos(6)
                        new_pos = (c[0] + L - 1, c[1] + nopos[0])
                        norient = 0
                    case (1, 6):
                        # 6-bot
                        # emerge on top edge of 2
                        norient = 1
                        c = cell_to_pos(2)
                        new_pos = (c[0] + nopos[0], c[1])
                    case (2, 1):
                        # 1-left
                        # emerge on left edge of 4
                        c = cell_to_pos(4)
                        new_pos = (c[0], c[1] + L - nopos[1] - 1)
                        norient = 0
                    case (2, 3):
                        # 3-left
                        # emerge on top edge of 4
                        c = cell_to_pos(4)
                        new_pos = (c[0] + nopos[1], c[1])
                        norient = 1
                    case (2, 4):
                        # 4-left
                        # emerge on left edge of 1
                        c = cell_to_pos(1)
                        new_pos = (c[0], c[1] + L - nopos[1] - 1)
                        norient = 0
                    case (2, 6):
                        # 6-left
                        # emerge on top edge of 1
                        c = cell_to_pos(1)
                        new_pos = (c[0] + nopos[1], c[1])
                        norient = 1
                    case (3, 1):
                        # 1-top
                        # emerge on left edge of 6
                        c = cell_to_pos(6)
                        new_pos = (c[0], c[1] + nopos[0])
                        norient = 0
                    case (3, 2):
                        # 2-top
                        # emerge on bottom edge of 6
                        c = cell_to_pos(6)
                        new_pos = (c[0] + nopos[0], c[1] + L - 1)
                        norient = 3 
                    case (3, 4):
                        # 4-top
                        # emerge on left edge of 3
                        c = cell_to_pos(3)
                        new_pos = (c[0], c[1] + nopos[0])
                        norient = 0
                if get(board, new_pos) != BLOCKED:
                    pos = new_pos
                    orient = norient
                else:
                    break
            counter -= 1

ans2 = 1000*(pos[1] + 1) + 4*(pos[0] + 1) + orient
print(ans2)
