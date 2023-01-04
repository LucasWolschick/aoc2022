import sys
data = sys.stdin.readlines()
ops = []

for l in data:
    l = l.strip()
    if l != "":
        if l[:4] == "noop":
            ops.append(("noop",))
        elif l[:4] == "addx":
            n = int(l[5:])
            ops.append(("addx",n))

x = 1
cycle = 1

strengths = []
WIDTH = 40
HEIGHT = 8
screen = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

def do_cycle():
    global x
    global cycle
    global screen
    global strengths

    cycle += 1

    # part 1
    if (cycle - 20) % 40 == 0:
        strengths.append(cycle*x)

    # part 2
    y_s = (cycle-1)//40
    x_s = (cycle-1) % 40
    if x-1 <= x_s <= x+1:
        screen[y_s][x_s] = True

for op in ops:
    match op:
        case ("noop", ):
            do_cycle()
        case("addx", n):
            do_cycle()
            x += n
            do_cycle()

print(sum(strengths))
output = []
for row in screen:
    l = "".join("█" if c else " " for c in row)
    output.append(l)
print("\n".join(output))
