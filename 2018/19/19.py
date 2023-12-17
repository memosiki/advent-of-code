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

arch.reg[0] = 0  # task 2 = 1


# 19.1 = 0
# 19.2 = 1
# 21.1 = 12420065
# 21.2 = 1670686


def to_str(reg: list[int]) -> str:
    return " ".join(f"{num:<10}" for num in reg)


print(f"ip=0   {to_str(arch.reg)} INITIAL")
while True:
    ip = arch.reg[bound_reg]
    if ip >= len(instructions):
        # halt
        break
    instructions[ip](*params[ip])
    arch.reg[bound_reg] += 1
    print(f"{ip=:<3} {to_str(arch.reg)} {instructions[ip].__name__} {params[ip]}")

print(f"{arch.reg[0]=}")
