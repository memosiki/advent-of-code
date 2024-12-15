import sys
import io
from enum import StrEnum

import numpy as np
from aoc_glue.input import parse_np_matrix
from aoc_glue.pprint import pprint_matrix


class Actor(StrEnum):
    EMPTY = "."
    ROBOT = "@"
    STONE = "O"
    WALL = "#"


TURN = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

if __name__ == "__main__":
    data = iter(sys.stdin.readlines())
    field_data = io.StringIO()
    for line in data:
        if not line.rstrip():
            break
        field_data.write(line)
    field_data.seek(0)
    field = parse_np_matrix(fd=field_data, dtype=np.str_)
    path = "".join(line.rstrip() for line in data)

    [x], [y] = np.where(field == Actor.ROBOT)
    field[x, y] = Actor.EMPTY
    N, M = field.shape

    def slide(x, y, dx, dy, field) -> bool:
        # Slide continuous line of rocks in the way
        while field[x, y] == Actor.STONE:
            # never oob since field is surrounded by walls
            x += dx
            y += dy
        if field[x, y] == Actor.EMPTY:
            field[x, y] = Actor.STONE
            return True
        return False

    for step, dir in enumerate(path):
        dx, dy = TURN[dir]
        if slide(x + dx, y + dy, dx, dy, field):
            x, y = x + dx, y + dy
        field[x, y] = Actor.EMPTY
    total_gps = 0
    xs, ys = np.where(field == Actor.STONE)
    pprint_matrix(field)
    for x, y in zip(xs, ys):
        total_gps += 100 * x + y
    print("Total GPS metric", total_gps)
