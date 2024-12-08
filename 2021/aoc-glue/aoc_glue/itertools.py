import itertools
from collections import deque
from typing import Iterable, Generator


def npairwise[T](data: Iterable[T], batch: int = 2) -> Generator[tuple[T, ...]]:
    """ "ABCDEF", 3 -> "ABC", "BCD", "CDE", "DEF" """
    iterator = iter(data)
    sentinel = object()
    window = deque(itertools.islice(data, batch - 1), maxlen=batch)
    elem = next(iterator, sentinel)
    while elem is not sentinel:
        window.append(elem)
        yield tuple(window)
        elem = next(iterator, sentinel)
