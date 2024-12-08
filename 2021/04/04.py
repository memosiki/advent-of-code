import contextlib

import pandas as pd
import tqdm

DIM = 5


def read_card() -> pd.DataFrame:
    card = pd.DataFrame(0, index=range(DIM), columns=range(DIM))
    for i in range(DIM):
        card.iloc[i] = list(map(int, input().split()))
    return card


def read_all_cards() -> list[pd.DataFrame]:
    cards = []
    with contextlib.suppress(EOFError):
        while True:
            input()
            cards.append(read_card())
    return cards


if __name__ == "__main__":
    nums = list(map(int, input().split(",")))
    cards = read_all_cards()
    total_cards = len(cards)

    marks = [
        pd.DataFrame(False, index=range(DIM), columns=range(DIM), dtype=bool)
        for _ in range(total_cards)
    ]

    pending_cards = set(range(total_cards))
    won_cards = set()
    first = last = (cards[0], marks[0], 0)
    for num in tqdm.tqdm(nums):
        for i in pending_cards.copy():
            card, mark = cards[i], marks[i]
            mark |= card == num
            if mark.all(axis=0).any() or mark.all(axis=1).any():
                won_cards.add(i)
                pending_cards.remove(i)
                if len(won_cards) == 1:
                    first = card, mark, num
                if len(won_cards) == total_cards:
                    last = card, mark, num
        if len(won_cards) == total_cards:
            break

    cardf, markf, numf = first
    unselectedf = cardf * ~markf
    print("First winning card", cardf, sep="\n")
    print("First winning marks", cardf * markf, sep="\n")
    print("First winning num", numf)

    cardl, markl, numl = last
    unselectedl = cardl * ~markl
    print("Last winning card", cardl, sep="\n")
    print("Last winning marks", cardl * markl, sep="\n")
    print("Last winning num", numl)

    print()

    print("First score", unselectedf.sum().sum() * numf)
    print("Last score", unselectedl.sum().sum() * numl)

# too high 57408
