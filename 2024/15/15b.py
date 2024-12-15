import sys
import io
from enum import StrEnum
from itertools import product

import numpy as np
from aoc_glue.input import parse_np_matrix


class Actor(StrEnum):
    EMPTY = "."
    ROBOT = "@"
    BOXL = "["
    BOXR = "]"
    WALL = "#"


type Loc = tuple[int, int]

TURN = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def convert(line: str) -> str:
    return (
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    )


if __name__ == "__main__":
    data = iter(sys.stdin.readlines())
    field_data = io.StringIO()
    for line in data:
        if not line.rstrip():
            break
        field_data.write(convert(line))
    field_data.seek(0)
    field = parse_np_matrix(fd=field_data, dtype=np.str_)
    path = "".join(line.rstrip() for line in data)
    N, M = field.shape

    # field without boxes
    clean_field = np.empty_like(field)
    for x, y in product(range(N), range(M)):
        clean_field[x, y] = Actor.WALL if field[x, y] == Actor.WALL else Actor.EMPTY

    [x0], [y0] = np.where(field == Actor.ROBOT)
    field[x0, y0] = Actor.EMPTY

    def gather_pushees(x: int, y: int, dir, pushees: set[Loc], field):
        dx, dy = TURN[dir]
        # already processed
        if (x, y) in pushees:
            return
        if field[x, y] in (Actor.BOXL, Actor.BOXR):
            # apply to self
            pushees.add((x, y))
            # spread downstream
            gather_pushees(x + dx, y + dy, dir, pushees, field)

        if field[x, y] == Actor.BOXL:
            # spread push to second part
            gather_pushees(x, y + 1, dir, pushees, field)
        if field[x, y] == Actor.BOXR:
            gather_pushees(x, y - 1, dir, pushees, field)

    def is_valid_push(pushees: set[Loc], dx, dy, field) -> bool:
        # all boxes have non-walls ahead
        return all(field[x + dx, y + dy] != Actor.WALL for x, y in pushees)

    def gather_boxes(field) -> set[Loc]:
        # gather all box locations
        xs, ys = np.where((field == Actor.BOXL) | (field == Actor.BOXR))
        return {(x, y) for x, y in zip(xs, ys)}

    for step, dir in enumerate(path):
        dx, dy = TURN[dir]
        pushees = set()
        gather_pushees(
            x=x0 + dx,
            y=y0 + dy,
            dir=dir,
            pushees=pushees,
            field=field,
        )
        # nothing to push
        if not pushees:
            assert field[x0 + dx, y0 + dy] not in (Actor.BOXL, Actor.BOXR)
            # clear path
            if field[x0 + dx, y0 + dy] == Actor.EMPTY:
                x0, y0 = x0 + dx, y0 + dy
        # should push
        elif is_valid_push(pushees, dx, dy, field):
            # gather boxes
            all_boxes = gather_boxes(field)
            stationary_boxes = all_boxes - pushees

            # prepare new field
            new_field = clean_field.copy()

            # place unmoved boxes
            for x, y in stationary_boxes:
                new_field[x, y] = field[x, y]

            # place moved boxes
            for x, y in pushees:
                new_field[x + dx, y + dy] = field[x, y]

            # print("All boxes", all_boxes)
            # print("Pushees", pushees)
            # print("Stationary boxes", all_boxes - pushees)

            x0, y0 = x0 + dx, y0 + dy
            # switch to new canvas
            field = new_field
        # print('Step', step, "Direction", dir)
        # field[x0, y0] = Actor.ROBOT
        # pprint_matrix(field)
        # field[x0, y0] = Actor.EMPTY

    total_gps = 0

    xs, ys = np.where(field == Actor.BOXL)
    for x, y in zip(xs, ys):
        total_gps += 100 * x + y
    print("Total GPS metric", total_gps)
