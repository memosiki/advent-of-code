import re
import sys
from typing import List

import numpy as np
import pandas as pd

int_template = re.compile(r"(-?\d+)")


def parse_ints(line: str) -> List[int]:
    return list(map(int, int_template.findall(line)))


def parse_matrix(fd=sys.stdin) -> list[list[str]]:
    return [list(line.rstrip()) for line in fd]


def parse_np_matrix(fd=sys.stdin, dtype=int) -> np.ndarray:
    return np.array([list(map(dtype, line.rstrip())) for line in fd])


def parse_pd_matrix(fd=sys.stdin, dtype=int) -> pd.DataFrame:
    return pd.DataFrame([list(map(dtype, line.rstrip())) for line in fd])
