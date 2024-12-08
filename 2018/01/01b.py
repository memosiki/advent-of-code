import itertools
import sys

offsets = map(int, sys.stdin.readlines())

seen = set()
frq = 0
for offset in itertools.cycle(offsets):
    frq += offset
    if frq in seen:
        print(frq)
        break
    seen.add(frq)
