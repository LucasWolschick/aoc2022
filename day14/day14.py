import sys

EMPTY, SAND, WALL = [0, 1, 2]

def print_board(board, start=(0, 0), end=(999, 999)):
    lines = []
    for y in range(start[1], end[1]+1):
        line = board[y]
        s = ""
        for x in range(start[0], end[0]+1):
            ch = line[x]
            if ch == EMPTY:
                s += ' ' # '.'
            elif ch == SAND:
                s += '░' # 'o'
            elif ch == WALL:
                s += '█' # '#'
        lines.append(s)
    return "\n".join(lines)

def get_bounds(board):
    min_x = 1000
    min_y = 1000
    max_x = 0
    max_y = 0
    for (y, line) in enumerate(board):
        for (x, ch) in enumerate(line):
            if ch != EMPTY:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    return (min_x, min_y), (max_x, max_y)

# read input
curves = []
for curve in sys.stdin.readlines():
    curve = curve.strip()
    if curve != "":
        points = []
        for coord in curve.split(' -> '):
            l, r = coord.split(',')
            points.append((int(l), int(r)))
        curves.append(points)

# populate board
def plotLine(a, b):
    x0, y0 = a
    x1, y1 = b
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    while True:
        yield (x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error += dy
            x0 += sx
        if e2 <= dx:
            if y0 == y1:
                break
            error += dx
            y0 += sy

def make_board():
    board = [[EMPTY]*1000 for _ in range(1000)]
    for c in curves:
        for i in range(len(c)-1):
            start, end = c[i], c[i+1]
            for point in plotLine(start, end):
                board[point[1]][point[0]] = WALL
    return board


# part 1
origin = (500, 0)
board = make_board()
death_plane = get_bounds(board)[1][1]

def step_sand(board, pos):
    # step one down
    if board[pos[1]+1][pos[0]] == EMPTY:
        return (pos[0], pos[1] + 1)
    elif board[pos[1]+1][pos[0]-1] == EMPTY:
        return (pos[0] - 1, pos[1] + 1)
    elif board[pos[1]+1][pos[0]+1] == EMPTY:
        return (pos[0] + 1, pos[1] + 1)
    else:
        return pos

sand_pos = origin
grains = 0
while True:
    new_pos = step_sand(board, sand_pos)
    
    if new_pos[1] > death_plane:
        break
    
    if new_pos[0] == sand_pos[0] and new_pos[1] == sand_pos[1]:
        grains += 1
        board[sand_pos[1]][sand_pos[0]] = SAND
        sand_pos = origin
    else:
        sand_pos = new_pos

print(print_board(board, *get_bounds(board)))
print(grains)

# part 2
board = make_board()
death_plane = get_bounds(board)[1][1]
print(death_plane)
for x in range(500-death_plane-10, 500+death_plane+10):
    board[death_plane+2][x] = WALL

sand_pos = origin
grains = 0
while True:
    new_pos = step_sand(board, sand_pos)
    
    if new_pos == sand_pos:
        grains += 1
        board[sand_pos[1]][sand_pos[0]] = SAND

        if new_pos == origin:
            break

        sand_pos = origin
    else:
        sand_pos = new_pos

print(print_board(board, *get_bounds(board)))
print(grains)
