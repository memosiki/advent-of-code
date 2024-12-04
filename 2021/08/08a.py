import sys
from collections import Counter

digit_map = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}
if __name__ == "__main__":
    output = []
    for line in sys.stdin:
        words = line.rstrip().split(" ")
        output.extend(words[11:15])

    digit_repr = Counter(len(signals) for signals in output)

    ans = sum(digit_repr[signal] for signal in digit_map.values())

    print(ans)
