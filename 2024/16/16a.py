from enum import IntEnum
from queue import PriorityQueue

import numpy as np
from aoc_glue.input import parse_np_matrix

INF = 1 << 31 - 1


class Dir(IntEnum):
    H = 0
    V = 1


TURNCOST = 1000

if __name__ == "__main__":
    field = parse_np_matrix(dtype=np.str_)
    [x_start], [y_start] = np.where(field == "S")
    [x_end], [y_end] = np.where(field == "E")
    field: np.ndarray = field != "#"
    optimal_score = -1
    N, M = field.shape
    weights = np.full((N, M, 2), INF, dtype=np.int32)

    # Dijkstra
    pq = PriorityQueue()
    pq.put((0, Dir.H, x_start, y_start))
    pq.put((TURNCOST, Dir.V, x_start, y_start))

    weights[x_start, y_start, Dir.V] = 0
    weights[x_start, y_start, Dir.H] = TURNCOST

    while not pq.empty():
        weight0, dir, x0, y0 = pq.get()
        if (x0, y0) == (x_end, y_end):
            optimal_score = int(weight0)
            break
        if weights[x0, y0, dir] < weight0:
            continue

        x = x0 + 1
        y = y0
        weight = weight0 + 1 + 1000 * (dir == Dir.H)
        if x < N and field[x, y] and weights[x, y, Dir.V] > weight:
            weights[x, y, Dir.V] = weight
            pq.put((weight, Dir.V, x, y))
        x = x0 - 1
        y = y0
        weight = weight0 + 1 + 1000 * (dir == Dir.H)
        if x >= 0 and field[x, y] and weights[x, y, Dir.V] > weight:
            weights[x, y, Dir.V] = weight
            pq.put((weight, Dir.V, x, y))
        x = x0
        y = y0 + 1
        weight = weight0 + 1 + 1000 * (dir != Dir.H)
        if y < M and field[x, y] and weights[x, y, Dir.H] > weight:
            weights[x, y, Dir.H] = weight
            pq.put((weight, Dir.H, x, y))
        x = x0
        y = y0 - 1
        weight = weight0 + 1 + 1000 * (dir != Dir.H)
        if y >= 0 and field[x, y] and weights[x, y, Dir.H] > weight:
            weights[x, y, Dir.H] = weight
            pq.put((weight, Dir.H, x, y))

    print("Optimal score", optimal_score)

# 82464 too high
