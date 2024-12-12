from collections import defaultdict
from itertools import product

from aoc_glue.input import parse_np_matrix
import numpy as np

if __name__ == "__main__":
    field = parse_np_matrix(dtype=str)
    N, M = field.shape
    area = defaultdict(int)
    perimeter = defaultdict(int)

    components = np.zeros_like(field, dtype=int)
    curr_component = 1
    for x0, y0 in product(range(N), range(M)):
        if components[x0, y0]:
            continue
        curr_component += 1
        queue = [(x0, y0)]
        while queue:
            x, y = queue.pop()
            components[x, y] = curr_component
            for xi, yi in (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ):
                if (
                    0 <= xi < N
                    and 0 <= yi < M
                    and field[x, y] == field[xi, yi]
                    and not components[xi, yi]
                ):
                    components[xi, yi] = curr_component
                    queue.append((xi, yi))

    for x0, y0 in product(range(N), range(M)):
        area[components[x0, y0]] += 1
        for x, y in (
            (x0 - 1, y0),
            (x0 + 1, y0),
            (x0, y0 - 1),
            (x0, y0 + 1),
        ):
            if 0 <= x < N and 0 <= y < M:
                perimeter[components[x0, y0]] += components[x0, y0] != components[x, y]
            else:
                perimeter[components[x0, y0]] += 1
    # print("Area", area)
    # print("Perimeter", perimeter)
    price = 0
    for region in area:
        price += area[region] * perimeter[region]
    print("Price", price)
