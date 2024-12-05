import itertools
from itertools import product

import numpy as np
from aoc_glue.input import parse_np_matrix
from tqdm import tqdm

MAH_LAZOR = 9

if __name__ == "__main__":
    total_flashes = 0
    field = parse_np_matrix()
    n, m = field.shape

    for step in tqdm(itertools.count(1)):
        flashed = np.zeros_like(field, dtype=bool)
        field += 1

        for x0, y0 in product(range(n), range(m)):
            if not flashed[x0, y0] and field[x0, y0] > MAH_LAZOR:
                # bfs
                queue = [(x0, y0)]
                flashed[x0, y0] = True
                while queue:
                    x, y = queue.pop()
                    for i, j in (
                        (x - 1, y - 1),
                        (x - 1, y),
                        (x - 1, y + 1),
                        (x, y - 1),
                        (x, y + 1),
                        (x + 1, y - 1),
                        (x + 1, y),
                        (x + 1, y + 1),
                    ):
                        if not (0 <= i < n and 0 <= j < m):
                            continue
                        field[i, j] += 1
                        if not flashed[i, j] and field[i, j] > MAH_LAZOR:
                            flashed[i, j] = True
                            queue.append((i, j))
        # reset flashed
        field *= ~flashed

        if flashed.all():
            break
    print("All-bright step", step)
