from random import shuffle

from tqdm import tqdm

from aoc_glue.input import parse_ints


nanobots = []
with open("input", "r") as fd:
    for line in fd:
        nanobots.append(tuple(map(int, parse_ints(line))))


# nanobots.sort(key=lambda x: -x[3])
# x, y, z, r = nanobots[0]
# coverage = sum(
#     abs(xi - x) + abs(yi - y) + abs(zi - z) <= r for xi, yi, zi, _ in nanobots
# )


def intersecting(ax, ay, az, arx, ary, arz, bx, by, bz, brx, bry, brz):
    return (
        abs(ax - bx) <= abs(arx - brx)
        and abs(ay - by) <= abs(ary - bry)
        and abs(az - bz) <= abs(arz - brz)
    )


def intersection(ax, ay, az, arx, ary, arz, bx, by, bz, brx, bry, brz):
    # intersection of two manhattan spheres
    return (
        ax / 2 + bx / 2,
        ay / 2 + by / 2,
        az / 2 + bz / 2,
        abs(arx - brx) / 2,
        abs(ary - bry) / 2,
        abs(arz - brz) / 2,
    )


# def intersection(ax, ay, az, ar, bx, by, bz, br ):
#     return (
#             ax / 2 + bx / 2,
#             ay / 2 + by / 2,
#             az / 2 + bz / 2,
#             abs(ar - br) / 2,
#         )


def volume(_, _1, _2, rx, ry, rz):
    return rx * ry * rz


def dist(point1, point2):
    (x1, y1, z1) = point1
    (x2, y2, z2) = point2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


max_added = -1
max_intersection: tuple
RESHUFFLE_COUNT = 1
for _ in range(RESHUFFLE_COUNT):
    shuffle(nanobots)
    for idx in tqdm(range(len(nanobots)), ascii=True):
        ax, ay, az, ar = nanobots[idx]
        arx = ary = arz = ar
        added = {
            idx,
        }
        for count in range(len(nanobots)):
            # greedy choice
            max_volume = 0
            max_id = -1
            for i, (bx, by, bz, br) in enumerate(nanobots):
                if i not in added and intersecting(
                    ax, ay, az, arx, ary, arz, bx, by, bz, br, br, br
                ):
                    if (
                        volume(
                            *intersection(
                                ax, ay, az, arx, ary, arz, bx, by, bz, br, br, br
                            )
                        )
                        > max_volume
                    ):
                        max_volume = volume(
                            *intersection(
                                ax, ay, az, arx, ary, arz, bx, by, bz, br, br, br
                            )
                        )
                        max_id = i
            if max_id < 0:
                break
            bx, by, bz, br = nanobots[max_id]
            ax, ay, az, arx, ary, arz = intersection(
                ax, ay, az, arx, ary, arz, bx, by, bz, br, br, br
            )
            added.add(max_id)
        if len(added) >= max_added:
            max_added = len(added)
            max_intersection = ax, ay, az, arx, ary, arz
print(f"{max_added=}, {max_intersection=}")
