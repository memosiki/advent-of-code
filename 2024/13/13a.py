import sys
from itertools import batched

from aoc_glue.input import parse_ints

ACOST = 3
BCOST = 1
MAX_PRESSES = 100
INF = max(ACOST, BCOST) * (MAX_PRESSES + 1) + 10e5  # there must be a system to it
if __name__ == "__main__":
    total = 0
    for aline, bline, prizeline in batched(sys.stdin, 3, strict=True):
        sys.stdin.readline()  # empty line after input
        xstepa, ystepa = parse_ints(aline)
        xstepb, ystepb = parse_ints(bline)
        prizex, prizey = parse_ints(prizeline)

        min_tokens = INF
        a_presses = {}
        for i in range(MAX_PRESSES + 1):
            a_presses[(xstepa * i, ystepa * i)] = i
        for i in range(MAX_PRESSES + 1):
            if (prizex - xstepb * i, prizey - ystepb * i) in a_presses:
                min_tokens = min(
                    min_tokens,
                    BCOST * i
                    + ACOST * a_presses[(prizex - xstepb * i, prizey - ystepb * i)],
                )
        if min_tokens != INF:
            total += min_tokens
    print("Total", total)

# 23954 too low
