import functools
import operator
import sys
from itertools import product

import math
from aoc_glue.input import parse_ints
from tqdm import tqdm


def concatenate(lhs: int, rhs: int) -> int:
    # fyi: https://www.python.org/doc/essays/list2str/
    return lhs * 10 ** int(math.log10(rhs) + 1) + rhs


if __name__ == "__main__":
    total_2op = 0
    total_3op = 0

    for line in tqdm(sys.stdin):
        res, *args = parse_ints(line)
        # Part 1.
        for ops in product((operator.add, operator.mul), repeat=len(args)):
            it = iter(ops)
            num = functools.reduce(lambda a, b: next(it)(a, b), args)
            if num == res:
                total_2op += res
                total_3op += res
                break
        else:
            # Part 2.
            for ops in product(
                (concatenate, operator.add, operator.mul), repeat=len(args)
            ):
                it = iter(ops)
                num = functools.reduce(lambda a, b: next(it)(a, b), args)
                if num == res:
                    total_3op += res
                    break
    print("Total 2 ops", total_2op)
    print("Total 3 ops", total_3op)

# $ time python 07.py < input
# 850it [00:09, 92.18it/s]
# Total 2 ops 7579994664753
# Total 3 ops 438027111276610
# python 07.py < input  9.76s user 0.06s system 99% cpu 9.854 total
# $ python --version
# Python 3.10.14 (39dc8d3c85a7, Aug 30 2024, 08:27:45)
# [PyPy 7.3.17 with GCC 14.2.1 20240805]
