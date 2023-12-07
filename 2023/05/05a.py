import sys
from pprint import pprint

from typing import Iterable

_, seeds = input().split(": ")
seeds: Iterable[int] = map(int, seeds.split())

# list of tuples containing ranges and relating offset
relation_chain: list[set[tuple[range, int]]] = []

for line in sys.stdin:
    line = line.strip()
    # new section
    if not line:
        relation_chain.append(set())
        _ = input()
        continue
    dst, src, size = map(int, line.split())
    relation_chain[-1].add((range(src, src + size), dst-src))


def resolve_chain(loc: int) -> int:
    print(loc, end="")
    for mappings in relation_chain:
        for (loc_range, offset) in mappings:
            if loc in loc_range:
                loc += offset
                print("->", loc, end=" ")
                break
        else:
            print("->", loc, end=" ")

    print()
    return loc


nearest_seed = float("inf")
for seed in seeds:
    nearest_seed = min(nearest_seed, resolve_chain(seed))
print(nearest_seed)
