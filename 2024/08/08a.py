from itertools import combinations

import numpy as np
from aoc_glue.input import parse_np_matrix

EMPTY = "."
if __name__ == "__main__":
    field = parse_np_matrix(dtype=str)
    N, M = field.shape
    antinodes = set()
    for antenna in np.unique(field):
        if antenna == EMPTY:
            continue
        freq = np.column_stack(np.where(field == antenna))
        for lhs, rhs in combinations(freq, 2):
            antinodes.add(tuple(2 * lhs - rhs))
            antinodes.add(tuple(2 * rhs - lhs))
    valid_antinodes = sum(0 <= x < N and 0 <= y < M for x, y in antinodes)
    print("Antinodes", valid_antinodes)
