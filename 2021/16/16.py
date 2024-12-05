import operator
import sys
from functools import reduce
from typing import Callable, Self

from tabulate import tabulate


class Portioner:
    """Portions and consumes bits from data."""

    def __init__(self, data, total_bits):
        self.data = data
        self.offset = total_bits

    def get(self, n: int) -> int:
        self.offset -= n
        mask = (1 << n) - 1
        return (self.data & (mask << self.offset)) >> self.offset

    def slice(self, n) -> Self:
        return Portioner(self.get(n), n)

    def __bool__(self):
        return self.offset > 0


type TypeID = int

EOF: int = 0
LITERAL_TYPEID: TypeID = 4

operation: dict[TypeID, Callable[[int, ...], int]] = {
    0: lambda *x: sum(x),
    1: operator.mul,
    2: lambda *x: min(x),
    3: lambda *x: max(x),
    LITERAL_TYPEID: lambda x: x,
    5: operator.gt,
    6: operator.lt,
    7: operator.eq,
}


def parse(text: str) -> tuple[int, int]:
    total_bits = len(text) * 4
    data = int(text, base=0x10)

    version_sum = 0

    def process(port: Portioner) -> int:
        version = port.get(3)
        typeid = port.get(3)
        # print(f"Packet {typeid}, v{version}")

        nonlocal version_sum
        version_sum += version

        if typeid == LITERAL_TYPEID:
            num = 0
            while True:
                sign = port.get(1)
                quartet = port.get(4)
                num <<= 4
                num |= quartet
                if sign == EOF:
                    return num
        else:
            length_typeid = port.get(1)
            sub_rets = []
            if length_typeid == 0:
                sub_port = port.slice(port.get(15))
                # process all sub packets in designated bits
                while sub_port:
                    sub_rets.append(process(sub_port))
            else:
                sub_count = port.get(11)
                # process all N sub packets
                for _ in range(sub_count):
                    sub_rets.append(process(port))
            return int(reduce(operation[typeid], sub_rets))

    result = process(Portioner(data, total_bits))
    return version_sum, result


if __name__ == "__main__":
    table = []
    for line in sys.stdin:
        line = line.strip()
        vsum, res = parse(line)
        table.append((line[:30], vsum, res))
    print(tabulate(table, headers=["Packet", "Version sum", "Result"]))
