import sys
from collections import Counter, defaultdict
from itertools import pairwise

from tabulate import tabulate
from tqdm import tqdm

type Pair = tuple[str, str]
SENTINEL = "^"


def count_pairs(pairs: dict[Pair, int]) -> Counter[str]:
    total = Counter()
    for (a, b), count in pairs.items():
        total[a] += count
        total[b] += count
    return total


if __name__ == "__main__":
    mapping: dict[Pair, str] = {}
    polymer: list[str] = list((SENTINEL, *input(), SENTINEL))
    input()
    for line in sys.stdin:
        line = line.rstrip()
        a, b, *_, c = line
        mapping[(a, b)] = c

    curr_pairs: dict[Pair, int] = Counter(pairwise(polymer))
    next_pairs: dict[Pair, int] = defaultdict(int)
    STEPS = 40
    for step in tqdm(range(STEPS), miniters=1):
        for pair in curr_pairs:
            if pair in mapping:
                a, b, c = *pair, mapping[pair]
                next_pairs[(a, c)] += curr_pairs[pair]
                next_pairs[(c, b)] += curr_pairs[pair]
            else:
                next_pairs[pair] += curr_pairs[pair]
        curr_pairs, next_pairs = next_pairs, defaultdict(int)
    total_count = count_pairs(curr_pairs)
    del total_count[SENTINEL]
    print(
        tabulate(
            total_count.items(),
            headers=("X", "Total Count"),
            tablefmt="fancy_outline",
        )
    )
    (_, most), *_, (_, least) = Counter(total_count).most_common()
    assert most % 2 == 0 == least % 2
    print("Diff", most // 2 - least // 2)
