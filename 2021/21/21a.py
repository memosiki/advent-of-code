from tabulate import tabulate
from termcolor import colored

if __name__ == "__main__":
    # inputs
    start1 = 6
    start2 = 7

    WIN = 1000

    # residue = sum(dicerolls[turn]) % MOD
    DIE_RESIDUE1 = [6, 4, 2, 10, 8]
    DIE_RESIDUE2 = [5, 3, 1, 9, 7]
    WRAPS = 5

    # Все операции со счётом в пределах раунда -- система вычетов по 10, +1
    MOD = 10
    SHIFT = 1

    turn1 = turn2 = 0
    score1 = score2 = 0
    step1 = start1 - SHIFT
    step2 = start2 - SHIFT

    while True:
        step1 = (step1 + DIE_RESIDUE1[turn1 % WRAPS]) % MOD
        score1 += step1 + SHIFT
        turn1 += 1
        if score1 >= WIN:
            metric = score2 * (turn1 + turn2) * 3
            break

        step2 = (step2 + DIE_RESIDUE2[turn2 % WRAPS]) % MOD
        score2 += step2 + SHIFT
        turn2 += 1

        if score2 >= WIN:
            metric = score1 * (turn1 + turn2) * 3
            break

    print(
        tabulate(
            [
                [1, start1, turn1, score1, turn1 * 3],
                [2, start2, turn2, score2, turn2 * 3],
            ],
            headers=["Player", "Start", "Turns", "Score", "Rolls"],
            tablefmt="fancy_outline",
        )
    )
    print(colored("Winning metric", attrs=["bold"]), metric)
