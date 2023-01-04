import sys
import math
import re

ns = [int(n.strip()) for n in sys.stdin.readlines() if not n.isspace()]

def put(nums):
    print([n for n, i in nums])

def indexinto(l, i):
    le = len(l)
    return ((i - 1) % (le - 1)) + 1 

def shuffle(ns, times=1):
    # decorate
    nums = [(n, i) for i, n in enumerate(ns)]

    for _ in range(times):
        for i in range(len(nums)):
            # find the element
            elem = 0
            for pos, (_, idx) in enumerate(nums):
                if idx == i:
                    elem = pos
                    break

            # displace it.
            dx, _ = nums[elem]
            if dx != 0:
                base = indexinto(nums, elem + dx)
                nums.pop(elem)
                nums.insert(base, (dx, i))

    # undecorate
    nums = [n for n, i in nums]
    return nums

# part 1
def part1():
    nums = shuffle(ns)
    offset = nums.index(0)
    s = []
    for i in range(1000, 3001, 1000):
        s.append(nums[(offset + i) % len(nums)])
    print(s, sum(s))

def part2():
    KEY = 811589153
    nums = [n*KEY for n in ns]
    nums = shuffle(nums, 10)
    offset = nums.index(0)
    s = []
    for i in range(1000, 3001, 1000):
        s.append(nums[(offset + i) % len(nums)])
    print(s, sum(s))

part1()
part2()
