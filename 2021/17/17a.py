from aoc_glue.input import parse_ints

_, _, ty0, _ = parse_ints(input())
print("Max y", abs(ty0) * abs(ty0 + 1) // 2)
