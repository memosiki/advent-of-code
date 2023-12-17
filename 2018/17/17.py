import sys
from enum import IntEnum, auto

from queue import Queue

from aoc_glue.input import parse_ints

# Extracted from preprocessed input
x_min = 436
x_max = 642
y_min = 5
y_max = 2022

#  +1 are offsets for ranges, since _max is inclusive
y_max += 1
x_max += 1

# border_offset is the margin for water to flow down on the grid border (since x is kind of unbound)
border_offset = 1
x_max += border_offset

spring = (500, 0)


class Tile(IntEnum):
    CLAY = auto()
    STAGNANT_WATER = auto()
    SAND = auto()
    FLOWING_WATER = auto()


translate = {
    Tile.CLAY: "#",
    Tile.STAGNANT_WATER: "~",
    Tile.SAND: " ",
    Tile.FLOWING_WATER: "|",
}


class Direction(IntEnum):
    not_set = 0
    down = 1
    left = 2
    right = 3
    still = 4


grid: list[list[Tile]] = [[Tile.SAND] * x_max for _ in range(y_max)]
direction: list[list[Direction]] = [[Direction.not_set] * x_max for _ in range(y_max)]
for line in sys.stdin:
    if line[0] == "x":
        (x, y1, y2) = parse_ints(line)
        for y in range(y1, y2 + 1):
            grid[y][x] = Tile.CLAY
    else:
        (y, x1, x2) = parse_ints(line)
        for x in range(x1, x2 + 1):
            grid[y][x] = Tile.CLAY


def pprint():
    for y in range(y_max):
        for x in range(x_max):
            if direction[y][x] and grid[y][x] != Tile.STAGNANT_WATER:
                grid[y][x] = Tile.FLOWING_WATER
    for y in range(y_max):
        print(*map(translate.get, grid[y][x_min:]), sep="")
    print()

    for y in range(y_max):
        for x in range(x_max):
            if grid[y][x] == Tile.FLOWING_WATER:
                grid[y][x] = Tile.SAND


def can_flow(x, y):
    return 0 <= x < x_max and 0 <= y < y_max and grid[y][x] == Tile.SAND


def has_water(x, y):
    return direction[y][x] > Direction.not_set


def cant_flow(x, y):
    return not can_flow(x, y)


def flood(x, y) -> bool:
    """
    Try to flood enclosed level.
    """
    left, right = x, x
    while grid[y][left] != Tile.CLAY:
        if can_flow(left, y + 1):
            return False
        left -= 1

    while grid[y][right] != Tile.CLAY:
        if can_flow(right, y + 1):
            return False
        right += 1

    # within borders
    assert left >= x_min, (x, y)
    assert right < x_max - border_offset, (x, y)

    for x in range(left + 1, right):
        direction[y][x] = Direction.still
        assert grid[y][x] == Tile.SAND
        grid[y][x] = Tile.STAGNANT_WATER
        if has_water(x, y - 1):
            reflow.put((x, y - 1))
    return True


def flow(x, y):
    queue = Queue()
    queue.put((x, y))
    while not queue.empty():
        (x, y) = queue.get_nowait()
        if cant_flow(x, y):
            continue
        # overspill into infinity
        if y + 1 >= y_max:
            continue

        # trapped water
        if (
            direction[y][x] == Direction.left
            and cant_flow(x - 1, y)
            and cant_flow(x, y + 1)
        ):
            flood(x, y)
            continue
        if (
            direction[y][x] == Direction.right
            and cant_flow(x + 1, y)
            and cant_flow(x, y + 1)
        ):
            flood(x, y)
            continue
        if cant_flow(x, y + 1) and cant_flow(x - 1, y) and cant_flow(x + 1, y):
            grid[y][x] = Tile.STAGNANT_WATER
            direction[y][x] = Direction.still
            # has to be coming from above, since can't flow anywhere else
            reflow.put((x, y - 1))
            continue

        # flow lower
        if can_flow(x, y + 1):
            direction[y + 1][x] = Direction.down
            queue.put((x, y + 1))
            continue

        # flow right or left
        if (
            direction[y][x] != Direction.right
            and direction[y][x - 1] != Direction.right
            and can_flow(x - 1, y)
        ):
            direction[y][x - 1] = Direction.left
            queue.put((x - 1, y))
        if (
            direction[y][x] != Direction.left
            and direction[y][x + 1] != Direction.left
            and can_flow(x + 1, y)
        ):
            direction[y][x + 1] = Direction.right
            queue.put((x + 1, y))


reflow = Queue()
flow(*spring)

while not reflow.empty():
    flow(*reflow.get())

pprint()
total_water = sum(
    sum(direction[y][x] > 0 for x in range(x_max)) for y in range(y_min, y_max)
)
still_water = sum(
    sum(direction[y][x] == Direction.still for x in range(x_max))
    for y in range(y_min, y_max)
)
print("Total water", total_water)
print("Still water", still_water)
