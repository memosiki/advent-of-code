from tqdm import tqdm

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


def to_str(reg: list[int]) -> str:
    return " ".join(f"{num:<10}" for num in reg)


# print(f"ip=0   {to_str(arch.reg)} INITIAL")
max_iter = 10_000_000
for i in tqdm(range(max_iter), ascii=True):
    ip = arch.reg[bound_reg]
    instructions[ip](*params[ip])
    if ip == 12:
        # reg4_list.append(arch.reg[4])
        print(f"{arch.reg[5]:<10} {arch.reg[4]}")
        # print(f"{ip=:<3} {to_str(arch.reg)} {instructions[ip].__name__} {params[ip]}")

    arch.reg[bound_reg] += 1
# print(reg4_list)
# print(f"{len(reg4_list)=} {len(set(reg4_list))=}")
# #

# print("Total unique", len(seen_reg4), seen_order)
# print("Latest reg4", seen_order[-1])
