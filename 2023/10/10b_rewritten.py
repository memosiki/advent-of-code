from enum import Enum, auto

from aoc_glue.input import parse_matrix


class Direction(Enum):
    right = auto()
    left = auto()
    down = auto()
    up = auto()


def move_along(pipe, x, y, direction: Direction) -> (int, int, Direction):
    return {
        ("|", Direction.up): (x, y - 1, Direction.up),
        ("|", Direction.down): (x, y + 1, Direction.down),
        ("-", Direction.right): (x + 1, y, Direction.right),
        ("-", Direction.left): (x - 1, y, Direction.left),
        ("L", Direction.down): (x + 1, y, Direction.right),
        ("L", Direction.left): (x, y - 1, Direction.up),
        ("J", Direction.down): (x - 1, y, Direction.left),
        ("J", Direction.right): (x, y - 1, Direction.up),
        ("7", Direction.right): (x, y + 1, Direction.down),
        ("7", Direction.up): (x - 1, y, Direction.left),
        ("F", Direction.left): (x, y + 1, Direction.down),
        ("F", Direction.up): (x + 1, y, Direction.right),
    }[pipe, direction]


maze = parse_matrix()
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
        # if inside(x, y):
        #     return "#"
        return " "

    for y in range(M):
        print(*(to_char(x, y) for x in range(N)))


(x, y) = start
# Depending on what letter S should represent, change those
maze[y][x] = "|"
direction = Direction.down

pipe = maze[y][x]
loop[y][x] = True

while True:
    x, y, direction = move_along(pipe, x, y, direction)
    loop[y][x] = True
    pipe = maze[y][x]
    if (x, y) == start:
        break

enclosed_space = 0
orthogonal = ("L", "J", "|")
for y in range(M):
    """
    Trace a ray from (x,0) to (x, N). Count how many times loop is intersected.
    """
    intersections = 0
    for x in range(N):
        if loop[y][x]:
            intersections += maze[y][x] in orthogonal
        else:
            enclosed_space += intersections % 2
pprint()
print("Enclosed", enclosed_space)
