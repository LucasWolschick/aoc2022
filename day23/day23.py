import sys
import math

grid = set()
WIDTH = 0
HEIGHT = 0
for y, l in enumerate(sys.stdin.readlines()):
    if l.strip() != "":
        WIDTH = len(l.strip())
        for x, c in enumerate(l.strip()):
            if c == "#":
                grid.add((x, y))
        HEIGHT = y+1
print(WIDTH, HEIGHT)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

N = (0, -1)
W = (-1, 0)
E = (1, 0)
S = (0, 1)
NW = add(N, W)
NE = add(N, E)
SE = add(S, E)
SW = add(S, W)

def move(grid, at, r):
    n = add(N, at) in grid 
    nw = add(NW, at) in grid 
    ne = add(NE, at) in grid 
    s = add(S, at) in grid 
    sw = add(SW, at) in grid 
    se = add(SE, at) in grid
    w = add(W, at) in grid 
    e = add(E, at) in grid

    if not (n or nw or ne or s or sw or se or w or e):
        return (0, 0)

    dirs = [
        (N, n or ne or nw),
        (S, s or se or sw),
        (W, w or nw or sw),
        (E, e or ne or se),
    ]
    for i in range(len(dirs)):
        d, occupied = dirs[(i + r) % len(dirs)]
        if not occupied:
            return d
    return (0, 0) 

def consider(grid, i):
    intents = {}
    for x, y in grid:
        dx, dy = move(grid, (x, y), i)
        if dx != 0 or dy != 0:
            tgt = (x + dx, y + dy)
            if not tgt in intents:
                intents[tgt] = [] 
            intents[tgt].append((x, y))
    return intents

def realize(grid, intents):
    moved = False

    for dest, from_list in intents.items():
        if len(from_list) == 1:
            grid.remove(from_list[0])
    
    for dest, from_list in intents.items():
        if len(from_list) == 1:
            grid.add(dest)
            moved = True

    return moved

def round(grid, i):
    intents = consider(grid, i)
    moved = realize(grid, intents)
    return moved

def bounds(grid):
    minx, miny = 1000, 1000 
    maxx, maxy = -1000, -1000 
    for x, y in grid:
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    return ((minx, miny), (maxx, maxy))

def print_grid(grid):
    l = []
    m, M = bounds(grid)
    for y in range(m[1], M[1] + 1):
        s = [] 
        for x in range(m[0], M[0] + 1):
            if (x, y) in grid:
               s.append('#')
            else:
                s.append('.')
        l.append("".join(s))
    print("\n".join(l))

# part 1

m, M = bounds(grid)
print((M[0] - m[0] + 1)*(M[1] - m[1] + 1) - len(grid))

i = 0
while round(grid, i):
    i += 1
    if i == 10:
        m, M = bounds(grid)
        print_grid(grid)
        print((M[0] - m[0] + 1)*(M[1] - m[1] + 1) - len(grid))

print_grid(grid)
print(i)
