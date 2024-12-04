import math
from collections import Counter
from itertools import product

import numpy as np
from aoc_glue.input import parse_np_matrix
from tqdm import tqdm

PEAK = 9
if __name__ == "__main__":
    field = parse_np_matrix()
    n, m = field.shape
    # Part 1. Lowest points
    lowest_points = []
    for x, y in tqdm(product(range(n), range(m)), total=n * m):
        if all(
            field[x, y] < field[i, j]
            for i, j in (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            )
            if 0 <= i < n and 0 <= j < m
        ):
            lowest_points.append((x, y))
    risk = sum(field[x, y] + 1 for x, y in lowest_points)

    # Part 2. Basins
    basins = np.zeros_like(field)
    for basin, (x, y) in tqdm(enumerate(lowest_points, start=1)):
        # bfs
        queue = [(x, y)]
        basins[x, y] = basin
        while queue:
            x, y = queue.pop()
            for i, j in (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ):
                if (
                    0 <= i < n
                    and 0 <= j < m
                    and not basins[i, j]
                    and field[x, y] <= field[i, j] < PEAK
                ):
                    basins[i, j] = basin
                    queue.append((i, j))
    basins_freq = Counter(basins.flatten())
    del basins_freq[0]  # peaks, not a basin

    print("Largest basins", basins_freq.most_common(3))
    print("Risk", risk)
    print("Product", math.prod(size for _, size in basins_freq.most_common(3)))

# too low 930600
