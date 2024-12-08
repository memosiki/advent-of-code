import sys
from collections import Counter
from typing import Sequence

import tabulate


def bit_frequency(nums: Sequence[int], pos) -> Counter[int]:
    freq_table = Counter()
    for num in nums:
        freq_table[num >> pos & 1] += 1
    return freq_table


if __name__ == "__main__":
    gamma = epsilon = oxygen_rating = co2_rating = 0
    nums = []
    bits = 0
    for line in sys.stdin:
        line = line.strip()
        bits = max(bits, len(line))
        nums.append(int(line, base=2))

    # epsilon, gamma
    for i in range(bits):
        count = bit_frequency(nums, i).most_common()
        [(g, _), (e, _), *_] = [*count, *count]
        gamma |= g << i
        epsilon |= e << i

    # oxygen
    oxygen_candidates = nums.copy()
    for i in reversed(range(bits)):
        count = bit_frequency(oxygen_candidates, i)
        flag = (count[0] <= count[1]) << i
        oxygen_candidates = [e for e in oxygen_candidates if e & 1 << i == flag]
        if len(oxygen_candidates) <= 1:
            break
    oxygen_rating = oxygen_candidates[0]

    # CO₂
    co2_candidates = nums.copy()
    for i in reversed(range(bits)):
        count = bit_frequency(co2_candidates, i)
        flag = (count[0] > count[1]) << i
        co2_candidates = [e for e in co2_candidates if e & 1 << i == flag]
        if len(co2_candidates) <= 1:
            break
    co2_rating = co2_candidates[0]

    print(
        tabulate.tabulate(
            (
                ("Gamma", gamma),
                ("Epsilon", epsilon),
                ("Oxygen generator rating", oxygen_rating),
                ("CO₂ scrubber rating", co2_rating),
                (),  # tabulate.SEPARATING_LINE,
                ("Consumption", gamma * epsilon),
                ("Life support rating", oxygen_rating * co2_rating),
            ),
            tablefmt="fancy_outline",
        )
    )
