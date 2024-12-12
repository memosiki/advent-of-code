import enum
from collections import defaultdict
from itertools import product

from aoc_glue.input import parse_np_matrix
import numpy as np


class Dir(enum.Enum):
    U = enum.auto()
    D = enum.auto()
    L = enum.auto()
    R = enum.auto()


steps = {
    Dir.U: (-1, 0),
    Dir.D: (1, 0),
    Dir.L: (0, -1),
    Dir.R: (0, 1),
}
steps_to_the_side = {
    Dir.U: (0, 1),
    Dir.D: (0, 1),
    Dir.L: (1, 0),
    Dir.R: (1, 0),
}

if __name__ == "__main__":
    field = parse_np_matrix(dtype=str)
    N, M = field.shape
    area = defaultdict(int)
    walls = defaultdict(set)

    components = np.zeros_like(field, dtype=int)
    curr_component = 0
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
    # add all walls
    for x0, y0 in product(range(N), range(M)):
        area[components[x0, y0]] += 1
        for dir, (step, stepy) in steps.items():
            x, y = x0 + step, y0 + stepy
            if (
                not (0 <= x < N and 0 <= y < M)
                or components[x0, y0] != components[x, y]
            ):
                walls[components[x0, y0]].add((dir, x0, y0))
    # merge walls
    uniq_walls = defaultdict(int)
    for region in walls:
        for dir, x0, y0 in walls[region]:
            x = x0 + steps_to_the_side[dir][0]
            y = y0 + steps_to_the_side[dir][1]
            if (dir, x, y) not in walls[region]:
                uniq_walls[region] += 1
    price = 0
    for region in area:
        price += area[region] * uniq_walls[region]
    print("Price", price)
