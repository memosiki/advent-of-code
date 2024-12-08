import sys
from collections import Counter


def invert(d: dict):
    return {val: key for key, val in d.items()}


couple, triple = 0, 0
for line in sys.stdin:
    counts = invert(Counter(line))
    couple += 2 in counts
    triple += 3 in counts

print(couple * triple)
