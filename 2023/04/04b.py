import sys

MAX_CARDS = 211
counts = [0] * MAX_CARDS

for card_id, card in enumerate(sys.stdin):
    description, submission = card.split("|")
    _, winning = description.split(":")
    winning_count = sum(1 for num in submission.split() if num in set(winning.split()))
    counts[card_id] += 1
    for i in range(card_id, card_id + winning_count):
        counts[i + 1] += counts[card_id]

print(sum(counts))
