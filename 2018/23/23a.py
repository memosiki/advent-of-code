from aoc_glue.input import parse_ints

nanobots = []
with open("input", "r") as fd:
    for line in fd:
        nanobots.append(tuple(parse_ints(line)))

nanobots.sort(key=lambda x: -x[3])
x, y, z, r = nanobots[0]
coverage = sum(
    abs(xi - x) + abs(yi - y) + abs(zi - z) <= r for xi, yi, zi, _ in nanobots
)
print("Max coverage", coverage)
