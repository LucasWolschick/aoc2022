data = []
try:
    while True:
        line = input().strip()
        if line != "":
            l, r = line.split(" ")
            data.append((l, r))
except EOFError:
    pass

# part 1
# A - X - rock
# B - Y - paper
# C - Z - scissors

def value(m):
    match m:
        case ('A', 'X'): return 1 + 3
        case ('A', 'Y'): return 2 + 6
        case ('A', 'Z'): return 3 + 0

        case ('B', 'X'): return 1 + 0
        case ('B', 'Y'): return 2 + 3
        case ('B', 'Z'): return 3 + 6

        case ('C', 'X'): return 1 + 6
        case ('C', 'Y'): return 2 + 0
        case ('C', 'Z'): return 3 + 3

print("part 1: ", sum(map(value, data)))

# part 2
# X - lose
# Y - tie
# Z - win

def value2(m):
    match m:
        case ('A', 'X'): return 3 + 0
        case ('B', 'X'): return 1 + 0
        case ('C', 'X'): return 2 + 0

        case ('A', 'Y'): return 1 + 3
        case ('B', 'Y'): return 2 + 3
        case ('C', 'Y'): return 3 + 3

        case ('A', 'Z'): return 2 + 6
        case ('B', 'Z'): return 3 + 6
        case ('C', 'Z'): return 1 + 6

print("part 2: ", sum(map(value2, data)))
