from itertools import product
from queue import PriorityQueue

import numpy as np
from aoc_glue.input import parse_np_matrix

# A*

INF = 1 << 31 - 1
REPS = 5
MAX_RISK = 9


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def clip(a):
    # risk clipping rules
    div, mod = divmod(a, MAX_RISK + 1)
    assert mod + div <= MAX_RISK
    return mod + div


def a_star(field: np.ndarray) -> None:
    n, m = field.shape
    weight = np.full(field.shape, INF, dtype=np.uint32)
    visited = np.zeros_like(field, dtype=np.bool)

    def heuristic(x, y, risk):
        # barely admissible
        return 1.5 * dist(x, y, n, m) + risk

    pq = PriorityQueue()

    pq.put((heuristic(0, 0, 0), (0, 0)))
    weight[0, 0] = 0
    while True:
        _, (x0, y0) = pq.get()
        visited[x0, y0] = True

        if (x0, y0) == (n - 1, m - 1):
            break

        risk = weight[x0, y0]
        for x, y in (
            (x0 - 1, y0),
            (x0 + 1, y0),
            (x0, y0 - 1),
            (x0, y0 + 1),
        ):
            if (
                0 <= x < n
                and 0 <= y < m
                and not visited[x, y]
                and risk + field[x, y] < weight[x, y]
            ):
                weight[x, y] = risk + field[x, y]

                pq.put((heuristic(x, y, weight[x, y]), (x, y)))

    print("Visited nodes", np.sum(visited))
    print("Optimal risk", weight[n - 1, m - 1])


if __name__ == "__main__":
    field = parse_np_matrix()
    x_tile, y_tile = field.shape
    # tile with increasing risk
    tiled_field = np.tile(field, (REPS, REPS))
    for i, j in product(range(REPS), range(REPS)):
        tiled_field[i * x_tile : (i + 1) * x_tile, j * y_tile : (j + 1) * y_tile] += (
            i + j
        )
    # roll over risk
    tiled_field = np.vectorize(clip)(tiled_field)
    assert (tiled_field <= 9).all()

    # Part 1.
    print("Single tile")
    a_star(field)
    print()
    # Part 2.
    print(f"Tiled x{REPS} field")
    a_star(tiled_field)
