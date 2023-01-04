import math
import sys
import collections

cubes = set()
for l in sys.stdin.readlines():
    if l.strip() != '':
        x, y, z = l.strip().split(",")
        cubes.add((int(x), int(y), int(z)))

# part 1
OFFSETS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
count = 0
for x, y, z in cubes:
    for dx, dy, dz in OFFSETS:
        if not ((x+dx, y+dy, z+dz) in cubes):
            count += 1

print(count)

# part 2
# estimate bounds for rocks
mn = (math.inf, math.inf, math.inf)
mx = (-math.inf, -math.inf, -math.inf)

for x, y, z in cubes:
    mn = (min(x, mn[0]), min(y, mn[1]), min(z, mn[2]))
    mx = (max(x, mx[0]), max(y, mx[1]), max(z, mx[2]))

# extend bounds by 1
mn = (mn[0] - 1, mn[1] - 1, mn[2] - 1)
mx = (mx[0] + 1, mx[1] + 1, mx[2] + 1)

# flood fill air
visited = set()
def bfs():
    print('doing bfs on volume', (mx[0]-mn[0])*(mx[1]-mn[1])*(mx[2]-mn[2]))
    visited.add(mn)
    q = collections.deque()
    q.append(mn)
    while len(q) > 0:
        vtx = q.popleft()
        for dx, dy, dz in OFFSETS:
            x, y, z = (vtx[0] + dx, vtx[1] + dy, vtx[2] + dz)
            if mn[0] <= x <= mx[0] and mn[1] <= y <= mx[1] and mn[2] <= z <= mx[2] and not ((x, y, z) in cubes) and not ((x, y, z) in visited):
               visited.add((x, y, z))
               q.append((x, y, z))

bfs()

# count faces which border flooded cells
count = 0
for x, y, z in cubes:
    for dx, dy, dz in OFFSETS:
        p = (x+dx, y+dy, z+dz)
        if not (p in cubes) and p in visited:
            count += 1

print(count)
