import sys

import tqdm

_, seeds = input().split(": ")
seeds = map(int, seeds.split())
seedgroups = []
for start, size in zip(seeds, iter(seeds)):
    seedgroups.append(tqdm.trange(start, start + size))

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


def resolve_chain(loc: int) -> int:
    for mappings in relation_chain:
        for loc_range, offset in mappings:
            if loc in loc_range:
                loc += offset
                break
    return loc


nearest = float("inf")

for seedrange in seedgroups:
    for seed in seedrange:
        nearest = min(nearest, resolve_chain(seed))
print(nearest)
