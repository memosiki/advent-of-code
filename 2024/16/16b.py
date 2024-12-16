from enum import IntEnum
from itertools import product
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
    N, M = field.shape

    def dijkstra(
        x_start, y_start, x_end, y_end, invert: bool
    ) -> tuple[int, np.ndarray]:
        pq = PriorityQueue()
        weights = np.full((N, M, 2), INF, dtype=np.int32)
        min_score = INF
        pq.put((0, Dir.H, x_start, y_start))
        weights[x_start, y_start, Dir.V] = 0
        if invert:
            pq.put((0, Dir.V, x_start, y_start))
            weights[x_start, y_start, Dir.H] = 0

        while not pq.empty():
            weight0, dir, x0, y0 = pq.get()
            if weight0 > min_score:
                break

            if (x0, y0) == (x_end, y_end):
                if invert:
                    weight0 += TURNCOST * (dir != Dir.H)
                min_score = min(min_score, weight0)
                if weight0 == min_score:
                    weights[x_end, y_end, dir != Dir.H] = min_score

            if weights[x0, y0, dir] < weight0:
                continue

            # vertical
            for x, y in (
                (x0 + 1, y0),
                (x0 - 1, y0),
            ):
                if 0 <= x < N and field[x, y]:
                    weight = weight0 + 1 + TURNCOST * (dir == Dir.H)
                    if weights[x, y, Dir.V] > weight:
                        weights[x, y, Dir.V] = weight
                        pq.put((weight, Dir.V, x, y))
                    weight = weight0 + 1 + TURNCOST * (dir == Dir.H) + TURNCOST
                    if weights[x, y, Dir.H] > weight:
                        weights[x, y, Dir.H] = weight
                        pq.put((weight, Dir.H, x, y))

            # horizontal
            for x, y in (
                (x0, y0 + 1),
                (x0, y0 - 1),
            ):
                if 0 <= y < M and field[x, y]:
                    weight = weight0 + 1 + TURNCOST * (dir != Dir.H)
                    if weights[x, y, Dir.H] > weight:
                        weights[x, y, Dir.H] = weight
                        pq.put((weight, Dir.H, x, y))
                    weight = weight0 + 1 + TURNCOST * (dir != Dir.H) + TURNCOST
                    if weights[x, y, Dir.V] > weight:
                        weights[x, y, Dir.V] = weight
                        pq.put((weight, Dir.V, x, y))
        return min_score, weights

    optimal_score, graph = dijkstra(x_start, y_start, x_end, y_end, invert=False)
    _, inv_graph = dijkstra(x_end, y_end, x_start, y_start, invert=True)
    total_seats = 0
    for x, y in product(range(N), range(M)):
        if graph[x, y, Dir.H] + inv_graph[x, y, Dir.H] == optimal_score:
            total_seats += 1
            continue
        if graph[x, y, Dir.V] + inv_graph[x, y, Dir.V] == optimal_score:
            total_seats += 1
    print("Optimal score", optimal_score)
    print("Total seats", total_seats)
