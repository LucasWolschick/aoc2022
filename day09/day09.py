import sys
dirs = []
for txt in sys.stdin.read().strip().splitlines():
    d, p = txt.split(' ')
    dirs.append((d, int(p)))

DIRECTIONS = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1)
}

# part 1
head = (0,0)
tail = head

def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

def adj(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) <= 1 and abs(ay - by) <= 1

def flush_tail(head, tail):
    if adj(head, tail):
        return tail

    if head[0] == tail[0]:
        # see if we need to move up or down
        if head[1] > tail[1]:
            # head is below tail, move tail down
            return (tail[0], tail[1] + 1)
        else:
            # head is above tail, move tail up
            return (tail[0], tail[1] - 1)
    elif head[1] == tail[1]:
        # see if we need to move left or right
        if head[0] > tail[0]:
            return (tail[0] + 1, tail[1])
        else:
            return (tail[0] - 1, tail[1])
    else:
        # we are neither adjacent nor aligned
        # move diagonally in whatever direction
        # makes us adjacent
        for d in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            testPos = (tail[0] + d[0], tail[1] + d[1])
            if adj(head, testPos):
                return testPos

    assert False

visited = set()
visited.add(tail)
for d in dirs:
    direction = DIRECTIONS[d[0]]
    movement = d[1]
    for _ in range(movement):
        head = (head[0] + direction[0], head[1] + direction[1])
        tail = flush_tail(head, tail)
        visited.add(tail)
print(len(visited))

# part 2
head = (0, 0)
knots = [(0, 0)] * 9
visited = set()
visited.add(knots[-1])
for d in dirs:
    direction = DIRECTIONS[d[0]]
    movement = d[1]
    for _ in range(movement):
        head = (head[0] + direction[0], head[1] + direction[1])
        knots[0] = flush_tail(head, knots[0])
        for i in range(1, len(knots)):
            knots[i] = flush_tail(knots[i-1], knots[i])
        visited.add(knots[-1])

print(len(visited))
