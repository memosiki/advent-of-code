import itertools

import numpy as np
from aoc_glue.input import parse_matrix
from numpy.typing import NDArray

galaxy: NDArray = np.array(parse_matrix()).T
EXPANSION_DIST = 1_000_000 - 1  # 2 - 1
empty_rows = np.apply_along_axis(np.all, 0, galaxy == ".").cumsum() * EXPANSION_DIST
empty_cols = np.apply_along_axis(np.all, 1, galaxy == ".").cumsum() * EXPANSION_DIST

planets = np.transpose((galaxy == "#").nonzero())

distance = 0
for (x1, y1), (x2, y2) in itertools.combinations(planets, 2):
    dist = (
        abs(x1 - x2)
        + abs(y1 - y2)
        + abs(empty_rows[y1] - empty_rows[y2])
        + abs(empty_cols[x1] - empty_cols[x2])
    )
    distance += dist
print(distance)
