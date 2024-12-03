import itertools
import operator
import sys
from collections import deque
from typing import Iterable, Generator, TextIO


# online-solution, like adaptive Huffman


def npairwise[T](data: Iterable[T], batch: int = 2) -> Generator[tuple[T, ...]]:
    iterator = iter(data)
    sentinel = object()
    window = deque(itertools.islice(data, batch - 1), maxlen=batch)
    elem = next(iterator, sentinel)
    while elem is not sentinel:
        window.append(elem)
        yield tuple(window)
        elem = next(iterator, sentinel)


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
