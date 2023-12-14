import arch
from aoc_glue.input import parse_ints

REG_NUM = 6
arch.reg = [0] * REG_NUM
instructions = []
params = []

with open("input", "r") as fd:
    bound_reg: int = parse_ints(fd.readline())[0]
    for line in fd:
        opcode_name, args = line.split(maxsplit=1)
        a, b, c = parse_ints(args)
        instructions.append(arch.opcodes[opcode_name])
        params.append((a, b, c))

while True:
    ip = arch.reg[bound_reg]
    if ip >= len(instructions):
        # halt
        break
    instructions[ip](*params[ip])
    arch.reg[bound_reg] += 1
    print(f"{ip=:<3} {str(arch.reg):<40} {instructions[ip].__name__} {params[ip]}")

print(f"{arch.reg[0]=}")
