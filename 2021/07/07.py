from typing import Callable, Iterable

from aoc_glue.input import parse_ints


def optimize[T](cost: Callable[[T, T], T], data: Iterable[T]) -> T:
    left = min(data)
    right = max(data)
    optimum = cost(left, right) * len(nums)
    for pos in range(left, right):
        local_cost = sum(cost(pos, num) for num in nums)
        optimum = min(local_cost, optimum)
    return optimum


if __name__ == "__main__":
    nums = parse_ints(input())

    # part 1.
    def constant_cost(a, b):
        return abs(a - b)

    # part 2.
    def linear_cost(a, b):
        n = abs(a - b)
        return n * (n + 1) // 2

    print("Optimal fuel with constant consumption", optimize(constant_cost, nums))
    print("Optimal fuel with linear consumption", optimize(linear_cost, nums))
