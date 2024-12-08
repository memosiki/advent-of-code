import sys
from itertools import pairwise
from typing import Sequence

from aoc_glue.input import parse_ints
from tqdm import tqdm


def safe(nums: Sequence[int]) -> bool:
    diffs = [a - b for a, b in pairwise(nums)]
    return all(1 <= abs(diff) <= 3 for diff in diffs) and (
        all(diff < 0 for diff in diffs) or all(diff > 0 for diff in diffs)
    )


def damp_safe(nums: list[int]) -> bool:
    # fixme: use linked list
    if safe(nums):
        return True
    for i in range(len(nums)):
        elem = nums.pop(i)
        if safe(nums):
            return True
        nums.insert(i, elem)
    return False


if __name__ == "__main__":
    total_safe = 0
    total_damp_safe = 0
    for line in tqdm(sys.stdin):
        nums = parse_ints(line)
        total_safe += safe(nums)
        total_damp_safe += damp_safe(nums)
    print("Total safe reports", total_safe)
    print("Total damp safe reports", total_damp_safe)
