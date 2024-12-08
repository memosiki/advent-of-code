import sys

import math
from aoc_glue.input import parse_ints
from tqdm import tqdm


def check(res: int, arg: int, *args: int) -> bool:
    # dfs expression tree

    if not args:
        return res == arg

    # mul *
    div, mod = divmod(res, arg)
    if not mod:
        found = check(div, *args)
        if found:
            return True

    # add +
    if res > arg:
        found = check(res - arg, *args)
        if found:
            return True

    # concat ||
    lhs, rhs = divmod(res, 10 ** int(math.log10(arg) + 1))
    if rhs == arg:
        found = check(lhs, *args)
        if found:
            return True

    return False


if __name__ == "__main__":
    total_3op = 0

    for line in tqdm(sys.stdin):
        res, *args = parse_ints(line)
        total_3op += res * check(res, *reversed(args))

    print("Total 3 ops", total_3op)

# $ time python 07dp.py < input
# 850it [00:00, 24411.37it/s]
# Total 3 ops 438027111276610
# python 07dp.py < input  1.52s user 0.03s system 378% cpu 0.408 total
# $ python --version
# Python 3.13.0
