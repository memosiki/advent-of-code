import sys

answer = 0
for card in sys.stdin:
    description, submission = card.split("|")
    _, winning = description.split(":")
    winning_count = sum(1 for num in submission.split() if num in set(winning.split()))
    answer += 2 ** (winning_count - 1) if winning_count else 0
print(answer)