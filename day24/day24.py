import sys
import math
from queue import PriorityQueue 

# parse input
# assume that (0,0) is located in position (1,1) in input
data = [l.strip() for l in sys.stdin.readlines() if not l.isspace()]
WIDTH = len(data[0])
HEIGHT = len(data)

class Blizzard:
    def __init__(self, offset, period, direction):
        self.offset = offset
        self.period = period
        self.direction = direction


b_rows = [[] for _ in range(HEIGHT)]
b_cols = [[] for _ in range(WIDTH)]
for y, row in enumerate(data):
    for x, col in enumerate(row):
        if col == ">":
            b_rows[y-1].append(Blizzard(x-1, WIDTH-2, 1))
        elif col == "<":
            b_rows[y-1].append(Blizzard(x-1, WIDTH-2, -1))
        elif col == "v":
            b_cols[x-1].append(Blizzard(y-1, HEIGHT-2, 1))
        elif col == "^":
            b_cols[x-1].append(Blizzard(y-1, HEIGHT-2, -1))

def is_stormed(pos):
    x, y, t = pos
    # verify row
    for b in b_rows[y]:
        if x == (b.offset + b.direction*t) % b.period:
            return True
    # verify column
    for b in b_cols[x]:
        if y == (b.offset + b.direction*t) % b.period:
            return True
    return False


# uniform cost search implementation
def adjacent(pos):
    neighbors = [
        (pos[0], pos[1], pos[2] + 1),
        (pos[0] + 1, pos[1], pos[2] + 1),
        (pos[0], pos[1] + 1, pos[2] + 1),
        (pos[0] - 1, pos[1], pos[2] + 1),
        (pos[0], pos[1] - 1, pos[2] + 1),
    ]
    valid = []
    for n in neighbors:
        x, y, t = n
        if (0 <= x < WIDTH-2 and 0 <= y < HEIGHT-2) or (x, y) == (0, -1) or (x, y) == (WIDTH-3, HEIGHT-2):
            # verify row cyclones
            if not is_stormed(n):
                valid.append(n)
    return valid

def print_board(t, marker=None):
    lines = []
    for y in range(HEIGHT):
        l = []
        if y == 0:
            l = ["#" + ("E" if marker==(0,-1,t) else ".") + "#"*(WIDTH-2)]
        elif y == HEIGHT-1:
            l = ["#"*(WIDTH-2) + ("E" if marker==(WIDTH-3, HEIGHT-2, t) else ".") + "#"]
        else:
            l = ["#"]
            for x in range(1, WIDTH-1):
                if is_stormed((x-1, y-1, t)):
                    l += ["x"]
                elif (x-1, y-1, t) == marker:
                    l += ["E"]
                else:
                    l += ["."]
            l += ["#"]
        lines.append("".join(l))
    print("\n".join(lines))

def ucs(v, tgt=(WIDTH-3, HEIGHT-2)):
    visited = set()
    q = PriorityQueue()
    q.put((0, v, [v]))
    
    while not q.empty():
        f, current_node, path = q.get()
        if current_node not in visited:
            visited.add(current_node)

            if (current_node[0], current_node[1]) == tgt:
                return path
            else:
                for neighbor in adjacent(current_node):
                    if neighbor not in visited:
                        q.put((f + 1, neighbor, path + [neighbor]))
    return None

# part 1
forward = ucs((0,-1,0), (WIDTH-3, HEIGHT-2))
print(len(forward)-1)

# part 2
backward = ucs(forward[-1], (0, -1))
forwardagain = ucs(backward[-1], (WIDTH-3, HEIGHT-2))
print(len(forward) + len(backward) + len(forwardagain) - 3)
