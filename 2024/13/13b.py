import sys
from itertools import batched

from aoc_glue.input import parse_ints

ACOST = 3
BCOST = 1
OFFSET = int(1e13)
if __name__ == "__main__":
    total = 0
    for aline, bline, prizeline in batched(sys.stdin, 3, strict=True):
        sys.stdin.readline()
        a1, a2 = parse_ints(aline)
        b1, b2 = parse_ints(bline)
        c1, c2 = parse_ints(prizeline)
        # general form
        c1 = -c1 - OFFSET
        c2 = -c2 - OFFSET

        # line intersection
        a0, amod = divmod(b1 * c2 - b2 * c1, a1 * b2 - a2 * b1)
        if amod != 0:
            continue
        b0, bmod = divmod(c1 * a2 - c2 * a1, a1 * b2 - a2 * b1)
        if bmod != 0:
            continue
        total += ACOST * a0 + BCOST * b0
    print("Total", total)
