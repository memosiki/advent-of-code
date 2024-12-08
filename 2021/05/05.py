import enum
from typing import Iterable

import sys

import pandas as pd
from tqdm import tqdm
from aoc_glue.input import parse_ints


def sign(x):
    if x == 0:
        return 0
    return -1 if x < 0 else 1


class Dir(enum.Enum):
    horizontal = enum.auto()
    vertical = enum.auto()
    diagonal = enum.auto()


def direction(x1, y1, x2, y2) -> Dir:
    if x1 == x2:
        return Dir.vertical
    if y1 == y2:
        return Dir.horizontal
    return Dir.diagonal


def get_line[T: int](x1, y1, x2, y2) -> Iterable[tuple[T, T]]:
    stepx = sign(x2 - x1)
    stepy = sign(y2 - y1)
    # vertical
    if not stepx:
        yrange = range(y1, y2 + stepy, stepy)
        return ((x1, y) for y in yrange)
    # horizontal
    if not stepy:
        xrange = range(x1, x2 + stepx, stepx)
        return ((x, y1) for x in xrange)
    # diagonal
    xrange = range(x1, x2 + stepx, stepx)
    yrange = range(y1, y2 + stepy, stepy)
    # guaranteed to be the same length by 45-degree angle
    return zip(xrange, yrange, strict=True)


DIM = 1000
if __name__ == "__main__":
    orthogonal_field = pd.DataFrame(0, index=range(DIM), columns=range(DIM))
    whole_field = pd.DataFrame(0, index=range(DIM), columns=range(DIM))

    for line in tqdm(sys.stdin):
        coords = parse_ints(line)
        # print(coords, *get_line(*coords), direction(*coords))

        for x, y in get_line(*coords):
            whole_field.loc[y, x] += 1
        if direction(*coords) != Dir.diagonal:
            for x, y in get_line(*coords):
                orthogonal_field.loc[y, x] += 1
    # print(orthogonal_field)
    print("Overlapping points, only orthogonal", (orthogonal_field > 1).sum().sum())
    # print(whole_field)
    print("Overlapping points, all directions", (whole_field > 1).sum().sum())
