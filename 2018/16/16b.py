import sys

import arch
from aoc_glue.input import parse_ints

arch.reg = [0] * 4
for line in sys.stdin:
    opcode, a, b, c = parse_ints(line)
    arch.reg[c] = arch.ops[opcode](a, b)

print(arch.reg[0])
