import sys
from collections import Counter

# map hand to integer
# requirements to mapping:
# - hand type precedence
# - equality for same position card in same type

alphabet = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"][::-1]
# mapping from hand to base13 integer
base = len(alphabet)
mapping = {letter: digit for digit, letter in enumerate(alphabet)}


def translate(hand: str) -> int:
    # map hand to base13 integer
    num = 1

    no_jacks = Counter(hand)
    del no_jacks["J"]

    # most common and second most common not counting jacks
    (_, most), (_, second), *_ = no_jacks.most_common(2) + [("", 0)] * 2
    jacks = Counter(hand)["J"]

    # 5 of a kind
    if most + jacks == 5:
        num *= 6
    # 4 of a kind
    elif most + jacks == 4:
        num *= 5
    # full house
    elif most + second + jacks == 5:
        num *= 4
    # 3 of a kind
    elif most + jacks == 3:
        num *= 3
    # two pair
    elif most + second + jacks == 4:
        num *= 2
    # 2 of a kind
    elif most + jacks == 2:
        num *= 1
    # 1 of a kind
    else:
        num *= 0

    for card in hand:
        num = num * base + mapping[card]
    return num


game: list[tuple[int, int]] = []
for line in sys.stdin:
    hand, bid = line.split()
    game.append((translate(hand), int(bid)))

game.sort()
answer = sum(rank * bid for rank, (_, bid) in enumerate(game, start=1))

print(answer)
