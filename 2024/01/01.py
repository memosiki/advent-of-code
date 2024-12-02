import sys
from collections import defaultdict

from aoc_glue.input import parse_ints

if __name__ == "__main__":
    left, right = [], []
    occurrence = defaultdict(int)
    for line in sys.stdin:
        a, b = parse_ints(line)
        left.append(a)
        right.append(b)
        occurrence[b] += 1

    print("Total dist", sum(abs(a - b) for a, b in zip(sorted(left), sorted(right))))
    print("Similarity score", sum(a * occurrence[a] for a in left))
