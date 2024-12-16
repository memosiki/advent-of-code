from itertools import product
from typing import Generator
from tqdm import tqdm

from aoc_glue.input import parse_ints

if __name__ == "__main__":
    # target always to the right-down
    txmin, txmax, tymin, tymax = parse_ints(input())

    def series(dx, dy) -> Generator[tuple[int, int]]:
        x = 0
        y = 0
        while True:
            yield x, y
            x += dx
            y += dy
            if x > txmax or y < tymin:
                break
            dx -= 1 * (dx > 0)
            dy -= 1

    dXs = range(0, txmax * 2)
    dYs = range(tymin, abs(tymin))
    hits = 0
    for dx, dy in tqdm(product(dXs, dYs)):
        for x, y in series(dx, dy):
            if txmin <= x <= txmax and tymin <= y <= tymax:
                hits += 1
                break
    print("Hits", hits)
