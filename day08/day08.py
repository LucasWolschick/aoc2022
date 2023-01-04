import sys

class Tile:
    h: int
    s: int
    v: bool

    def __init__(self, h, v=False):
        self.h = h
        self.v = v
        self.s = 0

    def __repr__(self):
        return "" + str(self.h) + ("t" if self.v else "f")

data = sys.stdin.read().strip()
grid = []
for line in data.splitlines():
    l = []
    for c in line:
        n = int(c)
        l.append(Tile(n, False))
    grid.append(l)

width = len(grid[0])
height = len(grid)

# part 1
# lr
for i in range(height):
    maxHeight = -1 
    for j in range(width):
        if grid[i][j].h > maxHeight:
            grid[i][j].v = True
        maxHeight = max(maxHeight, grid[i][j].h)

# rl
for i in range(height):
    maxHeight = -1 
    for j in reversed(range(width)):
        if grid[i][j].h > maxHeight:
            grid[i][j].v = True
        maxHeight = max(maxHeight, grid[i][j].h)

# tb 
for j in range(width):
    maxHeight = -1 
    for i in range(height):
        if grid[i][j].h > maxHeight:
            grid[i][j].v = True
        maxHeight = max(maxHeight, grid[i][j].h)

# bt 
for j in range(width):
    maxHeight = -1 
    for i in reversed(range(height)):
        if grid[i][j].h > maxHeight:
            grid[i][j].v = True
        maxHeight = max(maxHeight, grid[i][j].h)

visible = 0
for i in grid:
    for j in i: 
        if j.v:
            visible += 1
print(visible)


# part 2
def count(pos, direction, h):
    di, dj = direction
    i, j = pos
    i += di
    j += dj
    
    if not (0 <= i < height and 0 <= j < width):
        return 0
    elif grid[i][j].h >= h:
        return 1
    else:
        return 1 + count((i, j), direction, h)


biggest = 0
for i in range(height):
    for j in range(width):
        p = (i,j)
        h = grid[i][j].h 
        score = count(p, (1,0), h) * \
                count(p, (-1,0), h) * \
                count(p, (0,1), h) * \
                count(p, (0,-1), h)
        biggest = max(biggest, score)

print(biggest)
