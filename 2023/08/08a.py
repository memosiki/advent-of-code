import re
import sys
from itertools import cycle

directions = input()
input()
pattern = re.compile(r"(\w{3})")

instructions = {}
for line in sys.stdin:
    [src, dst1, dst2] = pattern.findall(line)
    instructions[src] = (dst1, dst2)

curr = "AAA"
steps = 1
for direction in cycle(directions):
    curr = instructions[curr][0 if direction == "L" else 1]
    print(curr)
    if curr == "ZZZ":
        break
    steps += 1

print(steps - 1)
