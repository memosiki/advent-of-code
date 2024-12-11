import math
from collections import Counter, defaultdict

from aoc_glue.input import parse_ints


STEPS = 75


def digit_count(n: int) -> int:
    return int(math.log10(n)) + 1


if __name__ == "__main__":
    stones = Counter(parse_ints(input()))
    for i in range(STEPS):
        next_stones = defaultdict(int)
        for stone, count in stones.items():
            if stone == 0:
                next_stones[1] += count
            elif (digits := digit_count(stone)) % 2 == 0:
                rhs, lhs = divmod(stone, 10 ** (digits // 2))
                next_stones[rhs] += count
                next_stones[lhs] += count
            else:
                next_stones[stone * 2024] += count
        stones = next_stones
    print("Total", sum(stones.values()))
