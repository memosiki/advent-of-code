import math
import sys

import numpy as np
from aoc_glue.input import parse_ints
from aoc_glue.pprint import pprint_spelled

# N = 11
N = 101
# M = 7
M = 103
STEPS = 100
if __name__ == "__main__":
    robots = []
    for line in sys.stdin:
        x, y, vx, vy = parse_ints(line)
        robots.append((x, y, vx, vy))
    for step in range(STEPS):
        for i, (x, y, vx, vy) in enumerate(robots):
            robots[i] = (x + vx) % N, (y + vy) % M, vx, vy
    canvas = np.zeros((N, M), dtype=np.int_)
    for x, y, _, _ in robots:
        canvas[x, y] += 1
    pprint_spelled(canvas, t=True)
    # quadrants
    q1 = canvas[: math.floor(N / 2), : math.floor(M / 2)].sum()
    q2 = canvas[math.ceil(N / 2) :, : math.floor(M / 2)].sum()
    q3 = canvas[: math.floor(N / 2), math.ceil(M / 2) :].sum()
    q4 = canvas[math.ceil(N / 2) :, math.ceil(M / 2) :].sum()
    safety_factor = q1 * q2 * q3 * q4
    print("Quadrants", q1, q2, q3, q4)
    print("Safety factor", safety_factor)
