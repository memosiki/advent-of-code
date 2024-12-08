import sys
from collections import Counter

from tqdm import tqdm

if __name__ == "__main__":
    mapping: dict[tuple[str, str], str] = {}
    polymer: list[str] = list(input())
    input()
    for line in sys.stdin:
        line = line.rstrip()
        a, b, *_, c = line
        mapping[(a, b)] = c

    STEPS = 10
    curr_polymer, next_polymer = polymer, []
    for step in tqdm(range(STEPS), miniters=1):
        a = b = "\0"
        for char in curr_polymer:
            a, b = b, char
            if (a, b) in mapping:
                next_polymer.append(mapping[(a, b)])
                next_polymer.append(b)
            else:
                next_polymer.append(b)
        curr_polymer, next_polymer = next_polymer, []
        # print(step, "".join(curr_polymer))
    (_, most), *_, (_, least) = Counter(curr_polymer).most_common()
    print("Diff", most - least)
