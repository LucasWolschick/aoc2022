import re
import sys
import math
from heapq import heappush, heappop
from time import time

mapping = {}
flows = []
adj = []

for line in sys.stdin.readlines():
    m = re.search(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)
    if m:
        name = m.group(1)
        flow = int(m.group(2))
        connections = list(m.group(3).split(', '))

        mapping[name] = len(flows)
        flows.append(flow)
        adj.append(connections)

for i, adjs in enumerate(adj):
    adj[i] = [mapping[x] for x in adjs]

def bfs(adj, start):
    distance = [-1]*len(adj)
    distance[start] = 0
    q = [start]

    while q:
        v = q.pop(0)
        for a in adj[v]:
            if distance[a] == -1:
                distance[a] = distance[v] + 1
                q.append(a)

    return distance

# compute distances
# from_v -> to_v -> dist
distances = [[0]*len(adj) for _ in range(len(adj))]
for v in range(len(adj)):
    d = bfs(adj, v)
    distances[v] = d

def is_opened(opened, i):
    return opened & (1 << i) != 0

def set_opened(opened, i):
    return opened | (1 << i)

# part 1
def solve1(start, T, flows):
    max_flow = sum(flows)
    max_gas = 0
    max_rate_at_t = [0]*T
    
    # our search space is based on which valve we're opening next!
    # INVARIANT: we are at the start of minute T-t+1, no actions have been taken yet
    # this minute's gas has not been accounted yet
    # recurse returns the maximum pressure releasable in the remaining time
    def recurse(me, opened, t, gas):
        nonlocal max_gas

        if t == 0:
            if gas > max_gas:
                max_gas = gas
            return gas

        # quit early if we can't hope to make more than the most seen til now
        if gas + max_flow*t < max_gas:
            return gas 

        # how many gas we produce per minute.
        rate = 0
        for i, pressure in enumerate(flows):
            if is_opened(opened, i):
                rate += pressure

        # also quit early if our rate is not the best one we've seen yet
        # is this correct?
        if rate < max_rate_at_t[t-1]:
            return gas
        else:
            max_rate_at_t[t-1] = rate

        # option 1: don't do anything; wait until we're done
        opt = recurse(me, opened, 0, gas + rate*t)

        # option 2: open a valve
        for i in range(len(adj)):
            distance = distances[me][i]
            pressure = flows[i]
            time_to_open = distance + 1
            op = is_opened(opened, i)
            # opening a valve in the last minute does not yield anything
            if pressure > 0 and t-time_to_open >= 1 and not op:
                # try to open it...
                nopened = set_opened(opened, i)
                opt = max(opt, recurse(i, nopened, t-time_to_open, gas + rate*time_to_open))
        
        return opt

    return recurse(mapping[start], 0, T, 0)

ans1 = solve1("AA", 30, flows)
print(ans1)

def solve2(start, T, flows):
    valves = [i for i, f in enumerate(flows) if f > 0]

    def partition(s, l, r):
        # for each element, we can either put it on the left set or on the right set
        if s == []:
            yield (l, r)
        else:
            e = s[-1]
            yield from partition(s[:-1], l + [e], r)
            yield from partition(s[:-1], l, r + [e])

    s = 0
    for i, (l, r) in enumerate(partition(valves, [], [])):
        lf = [0]*len(flows)
        for lv in l:
            lf[lv] = flows[lv]
        rf = [0]*len(flows)
        for rv in r:
            rf[rv] = flows[rv]
        s = max(s, solve1(start, T, lf) + solve1(start, T, rf))


    return s


t = time()
print(solve2("AA", 26, flows), time() - t)
