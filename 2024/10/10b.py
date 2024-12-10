from itertools import product

from aoc_glue.input import parse_np_matrix
import numpy as np

PEAK = 9
START = 0
if __name__ == "__main__":
    field = parse_np_matrix()
    N, M = field.shape

    # O(pathlen*N) time, 0(N) space
    depth = np.zeros_like(field)
    depth += field == START
    for step in range(START, PEAK + 1):
        for x0, y0 in product(range(M), range(N)):
            if not field[x0, y0] == step:
                continue
            for x, y in (
                (x0 - 1, y0),
                (x0 + 1, y0),
                (x0, y0 - 1),
                (x0, y0 + 1),
            ):
                if 0 <= x < M and 0 <= y < N and field[x, y] == field[x0, y0] + 1:
                    depth[x, y] += depth[x0, y0]
    score = depth[np.where(field == PEAK)].sum()
    print("Score", score)
