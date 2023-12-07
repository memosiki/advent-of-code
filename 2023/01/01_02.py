from typing import Iterable

import pattern_search


def pprint(iteree: Iterable) -> None:
    print(''.join(f"{elem:>3}" for elem in iteree))


if __name__ == '__main__':
    text = "abcdabcabcdabcdab"
    pattern = "dabcdab"
    print(pattern_search.KnuthMorrisPrattSearch(pattern, text))
