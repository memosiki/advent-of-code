import functools
import operator
import sys

if __name__ == "__main__":
    answer = 0
    for game in sys.stdin:
        counts = {"red": 0, "green": 0, "blue": 0}
        game_decriptor, outcomes = game.rstrip().split(":")
        _, game_id = game_decriptor.split()
        for outcome in outcomes.split("; "):
            for colorpair in outcome.split(", "):
                count, color = colorpair.split()
                counts[color] = max(counts[color], int(count))
        answer += functools.reduce(operator.mul, counts.values())
    print(answer)
