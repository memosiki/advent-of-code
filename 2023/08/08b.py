import itertools
import re
import sys
from functools import reduce

directions = tuple(map(lambda x: x == "R", input()))
input()
pattern = re.compile(r"(\w{3})")

instructions = {}
for line in sys.stdin:
    [src, dst1, dst2] = pattern.findall(line)
    instructions[src] = (dst1, dst2)


def ends_with_Z(a: str):
    return a[2] == "Z"


def GCD(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def LCM(a, b):
    return a * b // GCD(a, b)


paths = filter(ends_with_Z, instructions.keys())
cycles = []
for path in paths:
    cycle = 1
    curr = path
    for direction in itertools.cycle(directions):
        curr = instructions[curr][direction]
        if ends_with_Z(curr):
            break
        cycle += 1
    cycles.append(cycle)

# rolling lcm
answer = reduce(LCM, cycles, 1)

print(answer)
