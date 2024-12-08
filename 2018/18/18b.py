import sys
from collections import Counter
from copy import deepcopy

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


def freeze(field):
    return tuple(tuple(line) for line in field)


def unfreeze(field):
    return list(list(line) for line in field)


next = deepcopy(field)

seen_fields = {}


def step(field, next) -> (list, bool):
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
    frozen_field = freeze(next)
    if frozen_field in seen_fields:
        return next, field, True

    seen_fields[frozen_field] = time
    return next, field, False


time = 0
while True:
    time += 1
    field, next, repeat = step(field, next)
    if repeat:
        break
total_time = 1000000000
time_to_field = {time: field for field, time in seen_fields.items()}

prev = seen_fields[freeze(field)]
total_time -= prev
cycle = time - prev
time = prev + total_time % cycle

field = time_to_field[time]

woods = sum(sum(field[x][y] == "|" for x in range(1, N - 1)) for y in range(1, N - 1))
lumberyards = sum(
    sum(field[x][y] == "#" for x in range(1, N - 1)) for y in range(1, N - 1)
)
print("Time", time, "Value", woods * lumberyards)
