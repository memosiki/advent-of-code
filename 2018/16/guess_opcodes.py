import re
import sys
from itertools import batched
from typing import Iterable

import arch

int_template = re.compile(r"(-?\d+)")


def parse_ints(line: str) -> Iterable[int]:
    return map(int, int_template.findall(line))


candidates = {i: set(arch.ops) for i in range(len(arch.ops))}
for before, instruction, after, *_ in batched(map(parse_ints, sys.stdin), 4):
    arch.reg = list(before)
    opcode, a, b, c = instruction
    res = tuple(after)[c]
    candidates[opcode] = {op for op in candidates[opcode] if op(a, b) == res}

while any(len(ops) > 1 for ops in candidates.values()):
    for opcode, ops in candidates.items():
        if len(ops) == 1:
            (op,) = ops
            for opcode_i, ops_i in candidates.items():
                if opcode_i != opcode and op in ops_i:
                    candidates[opcode_i].remove(op)

candidates = {i: op.__name__ for i, (op,) in candidates.items()}
print(candidates)
print(*candidates.values(), sep=", ")
