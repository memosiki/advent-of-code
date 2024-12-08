import itertools
import operator
import sys
from typing import Generator, TextIO

from aoc_glue.itertools import npairwise

# online-solution, like adaptive Huffman


def reader(fd: TextIO = sys.stdin) -> Generator[int]:
    for line in fd:
        yield int(line)


if __name__ == "__main__":
    # to be consumed asynchronously
    nums1, nums2 = itertools.tee(reader(), 2)

    # part 1
    inc = sum(itertools.starmap(operator.lt, itertools.pairwise(nums1)))
    print("Increments", inc)

    # part2
    winc = sum(sum(a) < sum(b) for a, b in npairwise(npairwise(nums2, 3), 2))
    print("Sliding window increments", winc)
