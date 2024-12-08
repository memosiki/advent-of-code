import itertools
import sys
from typing import Iterable

from tqdm import tqdm

signatures = {
    # sorted digit signals
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}
alphabet = "abcdefg"


def translate(digit, translation):
    return "".join(sorted(digit.translate(translation)))


def digits_to_int(digits: Iterable[int]) -> int:
    num = 0
    for digit in digits:
        num *= 10
        num += digit
    return num


if __name__ == "__main__":
    total = guesses = 0
    for line in (pbar := tqdm(sys.stdin)):
        words = line.rstrip().split(" ")
        digits = words[:10]
        output = words[11:15]
        for assumption in itertools.permutations(alphabet):
            guesses += 1
            mapping = "".join(assumption)
            translation = str.maketrans(mapping, alphabet)
            for digit in digits:
                if translate(digit, translation) not in signatures:
                    break
            else:
                num = digits_to_int(
                    signatures[translate(digit, translation)] for digit in output
                )
                total += num
                pbar.set_description_str(f"Guesses {guesses}")
                break
    print("Total", total)
