from collections import Counter
from functools import cache
from itertools import product

import numpy as np

if __name__ == "__main__":
    # inputs
    start1 = 6
    start2 = 7

    WIN = 21

    # All operations on shifts and board positions are  -- mod 10, +1
    # scores are normal integers
    MOD = 10
    SHIFT = 1

    DIE_SIDES = (1, 2, 3)
    ROLL_COUNT = 3
    MAX_ROLL = max(DIE_SIDES) * ROLL_COUNT
    MIN_ROLL = min(DIE_SIDES) * ROLL_COUNT

    ROLLS = Counter(sum(rolls) for rolls in product(DIE_SIDES, repeat=ROLL_COUNT))

    # board state map, depending on the roll[s]
    STATE = np.array(
        # roll - axis 1, prev board state - axis 0
        [[(board + roll) % MOD for roll in range(MAX_ROLL + 1)] for board in range(MOD)]
    )

    @cache
    def seek(score1, score2, board1, board2) -> (int, int):
        assert score1 < WIN
        if score2 >= WIN:
            return 0, 1
        win1 = win2 = 0
        for die1, count1 in ROLLS.items():
            board10 = STATE[board1, die1]
            score10 = score1 + board10 + SHIFT
            if score10 >= WIN:
                win1 += count1
                continue
            for die2, count2 in ROLLS.items():
                board20 = STATE[board2, die2]
                score20 = score2 + board20 + SHIFT
                win1 += count1 * count2 * seek(score10, score20, board10, board20)[0]
                win2 += count1 * count2 * seek(score10, score20, board10, board20)[1]
        return win1, win2

    wins = seek(0, 0, start1 - SHIFT, start2 - SHIFT)
    print("Wins", wins)
    print("Max", max(wins))
