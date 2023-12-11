import platform
import sys
from enum import Enum, auto

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
    start = "S"

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
            ("S", Direction.N): (x, y - 1, Direction.N),
            ("S", Direction.S): (x, y + 1, Direction.S),
        }[self, direction]


maze = [list(line.rstrip()) for line in sys.stdin]
N = len(maze)
start = (0, 0)
for y in range(N):
    for x in range(N):
        if maze[y][x] == Pipe.start:
            start = (x, y)

distance = 0
pipe = Pipe.start
direction = Direction.S
(x, y) = start
while True:
    x, y, direction = pipe.move_along(x, y, direction)
    distance += 1
    pipe = Pipe(maze[y][x])
    if pipe == Pipe.start:
        break

print("Total distance", distance)
print("Answer", distance // 2 + distance % 2)
