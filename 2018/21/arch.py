reg: list[int] = []


def addr(a, b, c):
    reg[c] = reg[a] + reg[b]


def addi(a, b, c):
    reg[c] = reg[a] + b


def mulr(a, b, c):
    reg[c] = reg[a] * reg[b]


def muli(a, b, c):
    reg[c] = reg[a] * b


def banr(a, b, c):
    reg[c] = reg[a] & reg[b]


def bani(a, b, c):
    reg[c] = reg[a] & b


def borr(a, b, c):
    reg[c] = reg[a] | reg[b]


def bori(a, b, c):
    reg[c] = reg[a] | b


def setr(a, _, c):
    reg[c] = reg[a]


def seti(a, _, c):
    reg[c] = a


def gtir(a, b, c):
    reg[c] = int(a > reg[b])


def gtri(a, b, c):
    reg[c] = int(reg[a] > b)


def gtrr(a, b, c):
    reg[c] = int(reg[a] > reg[b])


def eqir(a, b, c):
    reg[c] = int(a == reg[b])


def eqri(a, b, c):
    reg[c] = int(reg[a] == b)


def eqrr(a, b, c):
    reg[c] = int(reg[a] == reg[b])


# ordered by opcode number
ops = (
    eqri,
    bori,
    addi,
    bani,
    seti,
    eqrr,
    addr,
    gtri,
    borr,
    gtir,
    setr,
    eqir,
    mulr,
    muli,
    gtrr,
    banr,
)

opcodes = {op.__name__: op for op in ops}
