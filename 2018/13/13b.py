import sys

from sortedcontainers import SortedSet

track = [line for line in sys.stdin]
width: int = len(max(track, key=len))
height = len(track)
# Pad with spaces. Spaces at line ends tend to disappear
track = [list(line.rstrip().ljust(width)) for line in track]

# print(*track, sep="\n")
static_minecarts = {"^": "|", "<": "-", "v": "|", ">": "-"}
minecarts = SortedSet()  # order (x, y)
stats = {}  # (x, y) -> (turns, covers)

for x in range(width):
    for y in range(height):
        if track[y][x] in static_minecarts:
            minecarts.add((x, y))
            stats[(x, y)] = (0, static_minecarts[track[y][x]])


def move(direction, x, y) -> (int, int):
    match direction:
        case "^":
            return x, y - 1
        case ">":
            return x + 1, y
        case "<":
            return x - 1, y
        case "v":
            return x, y + 1
    assert False, direction


turn_map = {
    "<": {"+": {0: "v", 1: "<", 2: "^"}, "/": "v", "\\": "^"},
    "v": {"+": {0: ">", 1: "v", 2: "<"}, "/": "<", "\\": ">"},
    ">": {"+": {0: "^", 1: ">", 2: "v"}, "/": "^", "\\": "v"},
    "^": {"+": {0: "<", 1: "^", 2: ">"}, "/": ">", "\\": "<"},
}


def revolve(railway, direction, turns) -> (str, int):
    """returns (direction, turns_count)"""
    match railway:
        case "+":
            return turn_map[direction][railway][turns % 3], turns + 1
        case "/" | "\\":
            return turn_map[direction][railway], turns
        case _:
            return direction, turns


def pprint():
    for y in range(height):
        print(*(track[y][x] for x in range(width)), sep="")
    print()


while True:
    # pprint()
    next_minecarts = SortedSet()

    for x, y in minecarts:
        if (x, y) not in stats:
            # already collided
            continue
        turns, covers = stats[(x, y)]
        del stats[(x, y)]
        direction, track[y][x] = track[y][x], covers
        xprev, yprev = x, y
        (x, y) = move(direction, x, y)
        railway = track[y][x]
        if railway in static_minecarts:
            # Collision
            track[yprev][xprev] = covers
            track[y][x] = stats[(x, y)][1]
            del stats[(x, y)]
            # if len(stats) <= 1:
            #     break
            continue
        direction, turns = revolve(railway, direction, turns)
        covers, track[y][x] = track[y][x], direction
        next_minecarts.add((x, y))
        stats[(x, y)] = (turns, covers)
    minecarts = next_minecarts
    if len(stats) <= 1:
        (x, y) = minecarts.pop()
        break
# pprint()
print(x, y, sep=",")
