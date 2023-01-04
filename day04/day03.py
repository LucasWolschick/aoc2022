import re

# process data
pairs = []
try:
    while True:
        line = input().strip()
        if line != '':
            l, r = line.split(',')
            (ll, lr) = l.split('-')
            (rl, rr) = r.split('-')
            pairs.append(((int(ll), int(lr)), (int(rl), int(rr))))
except EOFError:
    pass

# part 1
def completely_contains(p) -> bool:
    l, r = p
    return (l[0] <= r[0] and r[1] <= l[1]) or (r[0] <= l[0] and l[1] <= r[1])

print("part 1: ", sum(map(int, map(completely_contains, pairs))))

# part 2
def overlaps(p) -> bool:
    l, r = p
    return not (l[1] < r[0] or r[1] < l[0])

print("part 2: ", sum(map(int, map(overlaps, pairs))))
