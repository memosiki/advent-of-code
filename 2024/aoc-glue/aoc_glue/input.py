import re
import sys
from typing import List


int_template = re.compile(r"(-?\d+)")


def parse_ints(line: str) -> List[int]:
    return list(map(int, int_template.findall(line)))


def parse_matrix(fd=sys.stdin) -> list[list[str]]:
    return [list(line.rstrip()) for line in fd]


def parse_np_matrix(fd=sys.stdin, dtype=int):
    import numpy as np

    return np.array([list(map(dtype, line.rstrip())) for line in fd])
