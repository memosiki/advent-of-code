from collections import Counter

from aoc_glue.input import parse_ints


def breed(fish: Counter[int], days: int) -> int:
    prev = fish
    curr = Counter()
    for _ in range(days):
        for age, count in prev.items():
            if age == 0:
                curr[6] += count
                curr[8] += count
            else:
                curr[age - 1] += count
        prev, curr = curr, Counter()
    return sum(prev.values())


if __name__ == "__main__":
    population = Counter(parse_ints(input()))
    print("Day 80", breed(population, 80))
    print("Day 256", breed(population, 256))
    print("Day 10'000", breed(population, 10_000))
