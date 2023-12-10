import sys
from enum import Enum, auto

import platform

if platform.python_implementation() == "PyPy":
    from strenum import StrEnum
else:
    from enum import StrEnum


class Direction(Enum):
    E = auto()
    W = auto()
    S = auto()
    N = auto()


class Pipe(StrEnum):
    vertical = "|"
    horizontal = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"

    none = "."

    def move_along(self, x, y, direction: Direction) -> (int, int, Direction):
        return {
            ("|", Direction.N): (x, y - 1, Direction.N),
            ("|", Direction.S): (x, y + 1, Direction.S),
            ("-", Direction.E): (x + 1, y, Direction.E),
            ("-", Direction.W): (x - 1, y, Direction.W),
            ("L", Direction.S): (x + 1, y, Direction.E),
            ("L", Direction.W): (x, y - 1, Direction.N),
            ("J", Direction.S): (x - 1, y, Direction.W),
            ("J", Direction.E): (x, y - 1, Direction.N),
            ("7", Direction.E): (x, y + 1, Direction.S),
            ("7", Direction.N): (x - 1, y, Direction.W),
            ("F", Direction.W): (x, y + 1, Direction.S),
            ("F", Direction.N): (x + 1, y, Direction.E),
        }[self, direction]


maze = [list(line.rstrip()) for line in sys.stdin]
M = len(maze)
N = len(maze[0])
loop = [[False] * N for _ in range(M)]
start = (0, 0)
for y in range(M):
    for x in range(N):
        if maze[y][x] == "S":
            start = (x, y)


def pprint():
    def to_char(x, y):
        if loop[y][x]:
            return maze[y][x]
        if inside(x, y):
            return "#"
        return " "

    for y in range(M):
        print(*(to_char(x, y) for x in range(N)))


def inside(x, y):
    """
    Trace a ray from (x,y) to (0, y). Count how many times loop is intersected.
    """
    count = 0
    #
    intersections = (("F", "J"), ("7", "L"), ("J", "F"), ("L", "7"))
    angles = ("F", "J", "L", "7")
    orthogonal = (*angles, "|")
    prev = None
    for xi in range(x):
        if loop[y][xi] and maze[y][xi] in orthogonal:
            if maze[y][xi] in angles:
                count += (prev, maze[y][xi]) in intersections
                prev = maze[y][xi] if not prev else None
            else:
                count += 1
    return count % 2


(x, y) = start
# Depending on what letter S should represent, change those
maze[y][x] = "|"
direction = Direction.S

pipe = Pipe(maze[y][x])
loop[y][x] = True

distance = 0
while True:
    x, y, direction = pipe.move_along(x, y, direction)
    loop[y][x] = True
    pipe = Pipe(maze[y][x])
    if (x, y) == start:
        break

enclosed_space = 0
for y in range(M):
    for x in range(N):
        if not loop[y][x]:
            enclosed_space += inside(x, y)

pprint()
print("Enclosed", enclosed_space)
