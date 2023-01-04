"""
    Monkey NUMBER:
        Starting items: [NUMBER, ] NUMBER
        Operation: new = old (*|+) (NUMBER|old)
        Test: divisible by NUMBER
            If true: throw to monkey NUMBER
            If false: throw to monkey NUMBER


"""

import sys
from typing import Tuple, Literal
from dataclasses import dataclass
from functools import reduce

data = sys.stdin.read().split("\n\n")

@dataclass
class Monkey:
    number: int
    items: list[int]
    operation: Tuple[Literal["*"] | Literal ["+"], int | Literal["old"]]
    conditional: Tuple[int, int, int]

def parse_monkey(s: str) -> Monkey:
    lines = [x.strip() for x in s.strip().splitlines() if x.strip() != ""]
    
    number = int(lines[0][7:-1])
    items = [int(x) for x in lines[1][16:].split(', ')]
    op = lines[2][21]
    assert op == "*" or op == "+"
    operand = lines[2][23:]
    if operand != "old":
        operand = int(operand)
    test_cond = int(lines[3][19:])
    true_dest = int(lines[4][25:])
    false_dest = int(lines[5][26:])
    
    return Monkey(number, items, (op, operand), (test_cond, true_dest, false_dest))


def turn(monkeys: list[Monkey], inspections: list[int], limit):
    for m in monkeys:
        # inspect items
        while len(m.items) > 0:
            item = m.items.pop(0)
            match m.operation:
                case ("*", "old"):
                    item *= item
                case ("+", "old"):
                    item += item
                case ("*", n):
                    item *= int(n)
                case ("+", n):
                    item += int(n) # pylance, stop complaining!!!
            item //= 3
            cond, true_to, false_to = m.conditional
            monkeys[true_to if item % cond == 0 else false_to].items.append(item % limit)
            inspections[m.number] += 1

def turn2(monkeys: list[Monkey], inspections: list[int], limit):
    for m in monkeys:
        # inspect items
        while len(m.items) > 0:
            item = m.items.pop(0)
            match m.operation:
                case ("*", "old"):
                    item *= item
                case ("+", "old"):
                    item += item
                case ("*", n):
                    item *= int(n)
                case ("+", n):
                    item += int(n) # pylance, stop complaining!!!
            cond, true_to, false_to = m.conditional
            recv = monkeys[true_to if item % cond == 0 else false_to]
            recv.items.append(item % limit)
            inspections[m.number] += 1

# part 1
monkeys = [parse_monkey(s) for s in data if s != ""]
ALL_PRODUCT = reduce(lambda x, y: x * y, (m.conditional[0] for m in monkeys), 1)
inspections = [0 for m in monkeys]
for i in range(20):
    turn(monkeys, inspections, ALL_PRODUCT)

inspections.sort()
print("Monkey business level:", inspections[-1] * inspections[-2])

# part 2
monkeys = [parse_monkey(s) for s in data if s != ""]
inspections = [0 for m in monkeys]
for i in range(1, 10001):
    turn2(monkeys, inspections, ALL_PRODUCT)
    if i == 1 or i == 20 or i % 1000 == 0:
        print("== After round %d ==" % (i,))
        for m in monkeys:
            print("Monkey %d inspected items %d times." % (m.number, inspections[m.number]))

inspections.sort()
print(inspections)
print("New monkey business level:", inspections[-1] * inspections[-2])

