from collections import Counter

from tqdm import tqdm

from aoc_glue.input import parse_ints

nanobots = []
with open("input", "r") as fd:
    for line in fd:
        nanobots.append(tuple(map(int, parse_ints(line))))


def covered(point, sphere) -> bool:
    ax, ay, az, ar = sphere
    bx, by, bz = point
    return (
        abs(ax - bx) <= abs(ar) and abs(ay - by) <= abs(ar) and abs(az - bz) <= abs(ar)
    )


def dist(x1, y1, z1, x2, y2, z2):
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# how many times each point covered
covers = Counter()
for x, y, z, r in tqdm(nanobots):
    # every corner of sphere
    for point in (
        (x + r, y + r, z + r),
        (x + r, y + r, z - r),
        (x + r, y - r, z + r),
        (x + r, y - r, z - r),
        (x - r, y + r, z + r),
        (x - r, y + r, z - r),
        (x - r, y - r, z + r),
        (x - r, y - r, z - r),
    ):
        for nanobotL in nanobots:
            covers[point] += covered(point, nanobotL)

zero = (0, 0, 0)
print(f"{covers.most_common(1)=}")
most_covered_corner = covers.most_common(1)[0][0]
print("Distance", dist(*zero, *most_covered_corner))

most_covered_corner = (30246671, 10562968, 29986395)
