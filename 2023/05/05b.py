import sys

MAX_VAL = int(1e100)
MIN_VAL = -MAX_VAL


def intersect(a: range, b: range) -> range:
    return range(max(a.start, b.start), min(a.stop, b.stop))


def offset_by(a: range, offset: int) -> range:
    return range(a.start + offset, a.stop + offset)


def difference(a: range, b: range) -> "tuple[*range]":
    # no overlap
    if not intersect(a, b):
        return (a,)
    # a fully covers b
    if a.start <= b.start and a.stop >= b.stop:
        return tuple(filter(bool, (range(a.start, b.start), range(b.stop, a.stop))))
    # b fully covers a
    if b.start <= a.start and b.stop >= a.stop:
        return tuple()
    # b overlaps left
    if b.start <= a.start and b.stop < a.stop:
        return range(b.stop, a.stop),
    # b overlaps right
    if b.start > a.start and b.stop >= a.stop:
        return range(a.start, b.start),
    raise ValueError


def inverse(a: range) -> tuple[range, range]:
    return range(MIN_VAL, a.start), range(a.stop, MAX_VAL),


def difference2(a: range, b: range) -> "tuple[*range]":
    # a intersect not b
    left, right = inverse(b)
    return tuple(filter(bool, (intersect(a, left), intersect(a, right))))


_, seeds = input().split(": ")
seeds = map(int, seeds.split())

curr_groups: set[range] = set()
next_groups: set[range] = set()

for (start, size) in zip(seeds, iter(seeds)):
    curr_groups.add(range(start, start + size))

for line in sys.stdin:
    line = line.strip()
    # new section
    if not line:
        descriptor = input()
        # any remaining proceed untransformed
        curr_groups.update(next_groups)
        next_groups = set()
        continue
    dst, src, size = map(int, line.split())
    offset = dst - src
    group = range(src, src + size)
    for curr_group in curr_groups.copy():
        intersection = intersect(curr_group, group)
        if intersection:
            next_groups.add(offset_by(intersection, offset))
            curr_groups.remove(curr_group)
            remainder = difference(curr_group, group)
            if any(remainder):
                curr_groups.update(remainder)
curr_groups.update(next_groups)
print(min(*curr_groups, key=lambda x: x.start).start)
