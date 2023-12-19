from collections import Counter

from tqdm import tqdm

from aoc_glue.input import parse_ints
from ranges import Range, RangeDict

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


def dist(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def add_to_every_range(range: Range):
    for overlap in ranges.getoverlapranges(range):
        ranges[range & overlap] += 1


zero = (0, 0, 0)
ranges = RangeDict({"(-inf,+inf)": 0})
for x, y, z, r in tqdm(nanobots):
    nanobot = (x, y, z, r)
    min_dist = float("inf")
    max_dist = -1
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
        if covered(zero, nanobot):
            min_dist = 0
        min_dist = min(min_dist, dist(zero, point))
        max_dist = max(max_dist, dist(zero, point))
    add_to_every_range(Range(min_dist, max_dist, include_end=True))
counter = Counter()
for range, count in ranges.items():
    counter[tuple(range)] = count

print(counter.most_common(10))
# >>> [((RangeSet{Range[111927616, 224807769]},), 997), ((RangeSet{Range(224807769, 226401113]},), 996), ((RangeSet{Range(226401113, 229456529]},), 993), ((RangeSet{Range(229456529, 233909710]},), 992), ((RangeSet{Range(233909710, 235996343]},), 991), ((RangeSet{Range(235996343, 236397925]},), 990), ((RangeSet{Range(236397925, 236987484]},), 988), ((RangeSet{Range(236987484, 237824344]},), 987), ((RangeSet{Range[104730579, 111927616)},), 985), ((RangeSet{Range(237824344, 238611016]},), 984)]
