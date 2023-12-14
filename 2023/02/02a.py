import sys

if __name__ == "__main__":
    MAX_COUNTS = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    answer = 0
    for game in sys.stdin:
        valid = True
        game_decriptor, outcomes = game.rstrip().split(":")
        _, game_id = game_decriptor.split()
        for outcome in outcomes.split("; "):
            for colorpair in outcome.split(", "):
                count, color = colorpair.split()
                if int(count) > MAX_COUNTS[color]:
                    valid = False
                    break
        if valid:
            answer += int(game_id)
    print(answer)
