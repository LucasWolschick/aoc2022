import sys
import copy
import re

data = sys.stdin.read()
stacks_txt, info_txt, *_ = data.split('\n\n')

### parse instructions
# instructions are of the form: "move N from I to J"
pat = r"move (\d+) from (\d+) to (\d+)"
instructions = list(
    filter(lambda x: x,
        map(lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3))) if x else None,
            map(lambda x: re.search(pat, x.strip()),
                info_txt.splitlines()))))

### parse stacks
stacks_txt = stacks_txt.splitlines()
num_stacks = (len(stacks_txt[-1]) + 1)//4
stacks = [[] for _ in range(num_stacks)]
for line in reversed(stacks_txt[0:-1]):
    for i in range(num_stacks):
        ch = line[1 + 4*i]
        if ch != " ":
            stacks[i].append(ch)

### part 1: execute operations
stacks1 = copy.deepcopy(stacks)
for n, froms, tos in instructions:
    for i in range(n):
        if len(stacks1[froms-1]) > 0:
            s = stacks1[froms-1].pop()
            stacks1[tos-1].append(s)

string = "".join(map(lambda x: x[len(x)-1], stacks1))
print(string)

### part 2: execute operations
for n, froms, tos in instructions:
    slc = stacks[froms-1][-n:]
    stacks[froms-1][-n:] = []
    stacks[tos-1][len(stacks[tos-1]):] = slc

string = "".join(map(lambda x: x[len(x)-1], stacks))
print(string)
