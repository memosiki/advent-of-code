import sys
from pprint import pprint
from typing import Iterable

import tqdm

_, seeds = input().split(": ")
seeds = map(int, seeds.split())
seedgroups: list[range] = []
for (start, size) in zip(seeds, iter(seeds)):
    seedgroups.append(range(start, start + size))

# list of tuples containing ranges and relating offset
relation_chain: list[list[tuple[range, int]]] = []

for line in sys.stdin:
    line = line.strip()
    # new section
    if not line:
        relation_chain.append([])
        _ = input()
        continue
    dst, src, size = map(int, line.split())
    relation_chain[-1].append((range(src, src + size), dst - src))


def unresolve_chain(loc: int) -> int:
    for mappings in reversed(relation_chain):
        for (loc_range, offset) in mappings:
            if loc - offset in loc_range:
                loc -= offset
                break
    return loc


def unresolve_chain_print(loc: int) -> int:
    print(loc, end="")

    for mappings in reversed(relation_chain):
        for (loc_range, offset) in mappings:
            if loc - offset in loc_range:
                loc -= offset
                print("->", loc, end=" ")
                break
        else:
            print("->", loc, end=" ")
    print()
    return loc


# unresolve_chain(46)

nearest = float("inf")
max_dist = max(relation_chain[-1], key=lambda x: x[0].stop)[0].stop
for loc in tqdm.tqdm(range(max_dist, -1, -1)):
    seed = unresolve_chain(loc)
    for seedgroup in seedgroups:
        if seed in seedgroup:
            # unresolve_chain_print(loc)
            nearest = loc
print(nearest)
