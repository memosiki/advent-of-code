import sys

answer = 0
for line in sys.stdin:
    diffs: list[int] = list(map(int, line.split()))
    tails = [diffs[0]]
    while any(diffs):
        diffs = [b - a for a, b in zip(diffs, diffs[1:])]
        tails.append(diffs[0])
    answer += sum(tails[::2])
    answer += -sum(tails[1::2])
print(answer)
