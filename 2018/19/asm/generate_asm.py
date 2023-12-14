import re
from dataclasses import dataclass
from typing import Iterator
from uuid import uuid4

from jinja2 import BaseLoader, Environment


def parse_ints(line: str) -> Iterator[int]:
    return map(int, re.findall(r"(-?\d+)", line))


class DefaultList(list):
    def __getitem__(self, idx):
        return list(self)[idx] if idx < len(self) else -1


# instruction pointer register
ip_reg: str
# all registers
reg = DefaultList(["r10", "r11", "r12", "r13", "r14", "r15"])

with open("input", "r") as f:
    ip_id = next(parse_ints(f.readline()))
    ip_reg = reg[ip_id]
    input = f.readlines()

jinja_env = Environment(loader=BaseLoader())
template = jinja_env.from_string(
    """
extern printf, exit
section .rodata
    message db "Register value %#d", 10, 0
section .data
    instructions dq {{total_instructions}}
    instructions_count equ ($ - instructions) / 8
section .text

global main
main:
    ; elven asm instruction pointer
    xor rdi, rdi
    ; registers = r10 r11 r12 r13 r14 r15
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r13, r13
    xor r14, r14
    xor r15, r15
    mov r8, instructions_count

before_loop:
    cmp {{ip_reg}}, r8
    jge answer

    mov rax, 8
    mul {{ip_reg}}

    jmp [abs instructions + rax]

after_loop:
    inc {{ip_reg}}
    jmp before_loop

{% for item in instructions %}
{{ item.label }}: ;{{ item.elven_asm }}
    {% for item in item.asm_instructions %}{{ item }}
    {% endfor %}jmp after_loop
{% endfor %}

answer:
    sub   rsp, 8
    ; Call printf.
    mov   rsi, {{ip_reg}}
    lea   rdi, [rel message]
    xor   eax, eax
    call  printf

    ; Return from main.
    xor   eax, eax
    add   rsp, 8
    ret
"""
)


@dataclass
class Instruction:
    label: str
    elven_asm: str
    asm_instructions: list[str]

    def __init__(self, elven_code_line: str):
        opcode = elven_code_line.split()[0]
        # instruction parameters
        a, b, c = parse_ints(elven_code_line)
        self.elven_asm = elven_code_line
        label = f"{opcode}_{a}_{b}_{c}_{uuid4().hex:.4}"
        self.label = label

        # registers
        self.asm_instructions = {
            "seti": (f"mov {reg[c]}, {a}",),
            "setr": (f"mov {reg[c]}, {reg[a]}",),
            "addi": (
                f"mov {reg[c]}, {reg[a]}",
                f"add {reg[c]}, {b}",
            ),
            "addr": (
                f"mov {reg[c]}, {reg[a]}",
                f"add {reg[c]}, {reg[b]}",
            ),
            "mulr": (
                f"mov rax, {reg[b]}",
                f"mul {reg[a]}",
                f"mov {reg[c]}, rax",
            ),
            "muli": (
                f"mov rax, {b}",
                f"mul {reg[a]}",
                f"mov {reg[c]}, rax",
            ),
            "banr": (
                f"mov {reg[c]}, {reg[a]}",
                f"and {reg[c]}, {reg[b]}",
            ),
            "bani": (
                f"mov {reg[c]}, {b}",
                f"and {reg[c]}, {reg[a]}",
            ),
            "borr": (
                f"mov {reg[c]}, {reg[a]}",
                f"or {reg[c]}, {reg[b]}",
            ),
            "bori": (
                f"mov {reg[c]}, {b}",
                f"or {reg[c]}, {reg[a]}",
            ),
            "eqrr": (
                f"cmp {reg[a]}, {reg[b]}",
                f"je {label}_eq",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_eq: mov {reg[c]}, 1",
            ),
            "eqri": (
                f"cmp {reg[a]}, {b}",
                f"je {label}_eq",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_eq: mov {reg[c]}, 1",
            ),
            "eqir": (
                f"cmp {reg[b]}, {a}",
                f"je {label}_eq",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_eq: mov {reg[c]}, 1",
            ),
            "gtrr": (
                f"cmp {reg[b]}, {reg[a]}",
                f"jb {label}_gr",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_gr: mov {reg[c]}, 1",
            ),
            "gtri": (
                f"mov rax, {b}" f"cmp rax, {reg[a]}",
                f"jb {label}_gr",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_gr: mov {reg[c]}, 1",
            ),
            "gtir": (
                f"mov rax, {a}" f"cmp {reg[b]}, rax",
                f"jle {label}_gr",
                f"xor {reg[c]}, {reg[c]}",
                "jmp after_loop",
                f"{label}_gr: mov {reg[c]}, 1",
            ),
        }[opcode]


input = list(filter(bool, input))
instructions = []
for line in input:
    instructions.append(Instruction(line))

total_instructions = ", ".join(item.label for item in instructions)
asm = template.render(
    ip_reg=ip_reg,
    instructions=instructions,
    total_instructions=total_instructions,
)

with open("test.asm", "w") as f:
    f.writelines(asm)
