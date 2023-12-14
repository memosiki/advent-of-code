import sys
from collections import Counter
from copy import deepcopy

from tqdm import tqdm

field = [list(line.rstrip()) for line in sys.stdin]

# pad field with Nones
N = len(field)
field = [[None] + line + [None] for line in field]
N += 2
field = [[None] * N] + field + [[None] * N]


def count(x, y, field):
    return Counter(
        (
            field[x - 1][y - 1],
            field[x][y - 1],
            field[x + 1][y - 1],
            field[x - 1][y],
            field[x + 1][y],
            field[x - 1][y + 1],
            field[x][y + 1],
            field[x + 1][y + 1],
        )
    )


def pprint():
    for y in range(1, N - 1):
        print(*field[y][1 : N - 1], sep="")
    print()


next = deepcopy(field)
time = 10

for t in tqdm(range(time)):
    for x in range(1, N - 1):
        for y in range(1, N - 1):
            next[x][y] = field[x][y]
            surroundings = count(x, y, field)
            if field[x][y] == "." and surroundings["|"] >= 3:
                next[x][y] = "|"
            elif field[x][y] == "|" and surroundings["#"] >= 3:
                next[x][y] = "#"
            elif field[x][y] == "#" and not (
                surroundings["|"] >= 1 and surroundings["#"] >= 1
            ):
                next[x][y] = "."
    field, next = next, field
wooded = sum(sum(field[x][y] == "|" for x in range(1, N - 1)) for y in range(1, N - 1))
lumberyarded = sum(
    sum(field[x][y] == "#" for x in range(1, N - 1)) for y in range(1, N - 1)
)
print(wooded * lumberyarded)
