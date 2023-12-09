import sys

answer = 0
for line in sys.stdin:
    diffs: list[int] = list(map(int, line.split()))
    tails = [diffs[-1]]
    while any(diffs):
        diffs = [b - a for a, b in zip(diffs, diffs[1:])]
        tails.append(diffs[-1])
    answer += sum(tails)
print(answer)
# todo: https://www.youtube.com/watch?v=4AuV93LOPcE
