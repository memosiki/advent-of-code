from itertools import combinations

import numpy as np
from aoc_glue.input import parse_np_matrix

EMPTY = "."
if __name__ == "__main__":
    field = parse_np_matrix(dtype=str)
    N, M = field.shape

    def inbounds(x, y):
        return 0 <= x < N and 0 <= y < M

    antinodes = set()
    for antenna in np.unique(field):
        if antenna == EMPTY:
            continue
        freq = np.column_stack(np.where(field == antenna))
        for lhs, rhs in combinations(freq, 2):
            antinodes.add(tuple(lhs))
            antinodes.add(tuple(rhs))
            offset = rhs - lhs
            node = lhs.copy()
            while inbounds(*(node - offset)):
                node -= offset
                antinodes.add(tuple(node))
            node = rhs.copy()
            while inbounds(*(node + offset)):
                node += offset
                antinodes.add(tuple(node))

    # for node in antinodes:
    #     field[node] = '#'
    # pprint_matrix(field)
    print("Antinodes", len(antinodes))
