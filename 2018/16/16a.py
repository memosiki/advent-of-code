import sys
from itertools import batched

import arch
from aoc_glue.input import parse_ints

answer = 0
for before, instruction, after, *_ in batched(map(parse_ints, sys.stdin), 4):
    arch.reg = list(before)
    _, a, b, c = instruction
    res = tuple(after)[c]
    answer += sum(op(a, b) == res for op in arch.ops) >= 3
print(answer)
