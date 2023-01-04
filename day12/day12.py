import math
import sys

class Graph:
    def __init__(self, width, height):
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.start = (0, 0)
        self.finish = (0, 0)

    def from_input(s):
        lines = [l.strip() for l in s.strip().splitlines()]
        height = len(lines)
        width = len(lines[0])
        g = Graph(width, height)

        for y, line in enumerate(lines):
            for x, col in enumerate(line):
                if col == "S":
                    g.grid[y][x] = 0
                    g.start = (x, y)
                elif col == "E":
                    g.grid[y][x] = ord("z") - ord("a")
                    g.finish = (x, y)
                else:
                    g.grid[y][x] = ord(col) - ord("a")

        return g
    
    def __repr__(self):
        lines = []
        for l in self.grid:
            s = ""
            for c in l:
                s += "%2d " % (c,)
            lines.append(s)
        return "\n".join(lines)
    
    def adjacent(self, fromv, tov):
        hfrom = self.grid[fromv[1]][fromv[0]]
        hto = self.grid[tov[1]][tov[0]]
        return hto <= hfrom + 1
    
    def neighbors(self, pos):
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        for o in offsets:
            p = (pos[0] + o[0], pos[1] + o[1])
            if 0 <= p[0] < self.width and 0 <= p[1] < self.height and self.adjacent(pos, p):
                neighbors.append(p)
        return neighbors
    
    def djikstra(self, start, end):
        distances = [[math.inf for _ in range(self.width)] for _ in range(self.height)]
        previous = [[None for _ in range(self.width)] for _ in range(self.height)]
        q = set() 
        for y in range(self.height):
            for x in range(self.width):
                q.add((x, y))

        distances[start[1]][start[0]] = 0
        while len(q) > 0:
            mind = math.inf 
            u = None 
            for v in q:
                if u == None or distances[v[1]][v[0]] < mind:
                    mind = distances[v[1]][v[0]]
                    u = v
            q.remove(u)
            for v in self.neighbors(u):
                if v in q:
                    alt = distances[u[1]][u[0]] + 1
                    if alt < distances[v[1]][v[0]]:
                        distances[v[1]][v[0]] = alt
                        previous[v[1]][v[0]] = u
        
        u = end
        s = []
        if previous[u[1]][u[0]] or u == start:
            while u:
                s.insert(0, u)
                u = previous[u[1]][u[0]]
        return s
    
    def astar(self, start, end):
        openSet = {start}
        cameFrom = {}

        def h(a):
            return abs(a[0] - end[0]) + abs(a[1] - end[1])

        gScore = {}
        gScore[start] = 0

        fScore = {}
        fScore[start] = h(start) 

        while len(openSet) > 0:
            minf = math.inf
            current = None
            for v in openSet:
                f = fScore.get(v)
                if f and f < minf:
                    minf = f
                    current = v
            if current == end:
                break

            openSet.remove(current)
            for neighbor in self.neighbors(current):
                tentative_gScore = gScore.get(current, math.inf) + 1
                if tentative_gScore < gScore.get(neighbor, math.inf):
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + h(neighbor)
                    if not neighbor in openSet:
                        openSet.add(neighbor)

        u = end
        s = []
        if cameFrom.get(u) or u == start:
            while u:
                s.insert(0, u)
                u = cameFrom.get(u)
        return s

g = Graph.from_input(sys.stdin.read())
# print(g)

# part 1
print("part 1:", len(g.astar(g.start, g.finish)) - 1)

# part 2
minimal = math.inf
for y in range(g.height):
    for x in range(g.width):
        if g.grid[y][x] == 0:
            d = len(g.astar((x,y), g.finish)) - 1
            if d != -1 and d < minimal:
                minimal = d
print("part 2:", minimal)
