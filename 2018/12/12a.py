import sys
from collections import defaultdict


def translate(x: str) -> bool:
    return x == "#"


pots = list(map(translate, input().split()[2]))
rules = defaultdict(bool)

input()
for line in sys.stdin:
    [state, _, res] = line.split()
    rules[tuple(map(translate, state))] = translate(res)

# add some padding
curr = [False] * 2 * len(pots) + pots + [False] * 2 * len(pots)
offset = -2 * len(pots)


def repr(line, a, b):
    return "".join("#" if pot else "." for pot in line[a - offset : b - offset])


NUM_GENERATIONS = 20
for i in range(NUM_GENERATIONS):
    # print(i, repr(curr, -1, 35))
    next = [False] * len(curr)
    for i in range(2, len(curr) - 2):
        next[i] = rules[tuple(curr[i - 2 : i + 3])]
    curr = next

print(sum(i + offset for i in range(len(curr)) if curr[i]))
