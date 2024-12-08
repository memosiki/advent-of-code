import sys
from collections import Counter

# map hand to integer
# requirements to mapping:
# - hand type precedence
# - equality for same position card in same type

alphabet = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"][::-1]
# mapping from hand to base13 integer
base = len(alphabet)
mapping = {letter: digit for digit, letter in enumerate(alphabet)}


def translate(hand: str) -> int:
    # map hand to base13 integer

    num = 1
    # the most significant digit is the hand type
    match counts := Counter(hand).most_common(2):
        case [(_, 5)] | [(_, 4), _]:  # 4 or 5 of a kind
            num *= counts[0][1] + 2
        case [(_, 3), (_, 2)]:  # full house
            num *= 5
        case [(_, 3), _]:  # 3 of a kind
            num *= 4
        case [(_, 2), (_, 2)]:  # two pair
            num *= 3
        case _:  # 1 and 2 of a kind
            num *= counts[0][1]
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
