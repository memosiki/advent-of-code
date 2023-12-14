from functools import wraps

reg: list[int] = []


def can_fail(func):
    @wraps(func)
    def wrapper(a, b):
        try:
            return func(a, b)
        except IndexError:
            return None

    return wrapper


@can_fail
def addr(a, b):
    return reg[a] + reg[b]


@can_fail
def addi(a, b):
    return reg[a] + b


@can_fail
def mulr(a, b):
    return reg[a] * reg[b]


@can_fail
def muli(a, b):
    return reg[a] * b


@can_fail
def banr(a, b):
    return reg[a] & reg[b]


@can_fail
def bani(a, b):
    return reg[a] & b


@can_fail
def borr(a, b):
    return reg[a] | reg[b]


@can_fail
def bori(a, b):
    return reg[a] | b


@can_fail
def setr(a, _):
    return reg[a]


@can_fail
def seti(a, _):
    return a


@can_fail
def gtir(a, b):
    return int(a > reg[b])


@can_fail
def gtri(a, b):
    return int(reg[a] > b)


@can_fail
def gtrr(a, b):
    return int(reg[a] > reg[b])


@can_fail
def eqir(a, b):
    return int(a == reg[b])


@can_fail
def eqri(a, b):
    return int(reg[a] == b)


@can_fail
def eqrr(a, b):
    return int(reg[a] == reg[b])


# ordered by opcode
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
