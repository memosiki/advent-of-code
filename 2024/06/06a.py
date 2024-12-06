import numpy as np
from aoc_glue.input import parse_np_matrix
from aoc_glue.pprint import pprint_spelled

ROT = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

if __name__ == "__main__":
    map = parse_np_matrix(dtype=str)

    [x], [y] = np.where(map == "^")
    N, M = map.shape
    map[x, y] = "."
    field: np.ndarray[bool] = map == "."
    visited = np.zeros_like(field, dtype=np.bool)

    xstep, ystep = -1, 0
    visited[x, y] = True
    while 0 <= x + xstep < N and 0 <= y + ystep < M:
        while not field[x + xstep, y + ystep]:
            xstep, ystep = ROT[xstep, ystep]
        x, y = x + xstep, y + ystep
        visited[x, y] = True
    # pprint_spelled(field)
    pprint_spelled(visited)
    print("Total visited", np.sum(visited))
