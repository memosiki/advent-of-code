# ruff: noqa: F405,F403
from aoc_glue.input import parse_ints
from z3 import *

nanobots = []
with open("input", "r") as fd:
    for line in fd:
        nanobots.append(tuple(map(int, parse_ints(line))))


def dist(xa, ya, za, xb, yb, zb):
    return Abs(xa - xb) + Abs(ya - yb) + Abs(za - zb)


x, y, z = Int("x"), Int("y"), Int("z")
optimizer = Optimize()

coverage = Sum([dist(x, y, z, x1, y1, z1) <= r1 for (x1, y1, z1, r1) in nanobots])
# print(coverage)
distance_from_zero = dist(0, 0, 0, x, y, z)
# print(distance_from_zero)
optimizer.maximize(coverage)
optimizer.minimize(distance_from_zero)
optimizer.check()
model = optimizer.model()
print(model)
x, y, z = model[x].as_long(), model[y].as_long(), model[z].as_long()
# distance = solve(dist(*point, 0, 0, 0))
distance = abs(x) + abs(y) + abs(z)
print(f"{(x, y, z)=}, {distance=}")
