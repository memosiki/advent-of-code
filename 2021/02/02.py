import sys
from enum import StrEnum


class Dir(StrEnum):
    forward = "forward"
    up = "up"
    down = "down"


if __name__ == "__main__":
    h = aim = d1 = d2 = 0
    for line in sys.stdin:
        dir, num = line.split()
        steps = int(num)
        match dir:
            case Dir.up:
                d1 -= steps
                aim -= steps
            case Dir.down:
                d1 += steps
                aim += steps
            case Dir.forward:
                h += steps
                d2 += steps * aim
            case _:
                pass
    print(f"1. Position: {h=} {d1=}, {h*d1=}")
    print(f"2. Position: {h=} {d2=}, {h*d2=}")
