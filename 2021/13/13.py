import re
import sys

import numpy as np
from aoc_glue.input import parse_ints

if __name__ == "__main__":
    START_DIM = 2000

    def pprint(arr: np.ndarray):
        for row in np.vectorize(lambda x: "█" if x else "░")(np.transpose(arr)):
            print(*row, sep="")

    sheet = np.zeros((START_DIM, START_DIM), dtype=bool)
    folds = []
    for line in sys.stdin:
        nums = parse_ints(line)
        if not nums:
            break
        x, y = nums
        sheet[x, y] = True
    for line in sys.stdin:
        dir, num = re.search(r"fold along ([xy])=(\d+)", line).groups()
        folds.append((1 if dir == "y" else 0, int(num)))

    # folding

    def fold(paper, axis, pos):
        if axis == 0:
            # reshape, remove hanging stripes
            paper = paper[: pos * 2 + 1, :]
            # fold
            paper = paper[:pos, :] | paper[pos + 1 :, :][::-1, :]
        else:
            paper = paper[:, : pos * 2 + 1]
            paper = paper[:, :pos] | paper[:, pos + 1 :][:, ::-1]
        return paper

    # Part 1.
    for axis, pos in folds[:1]:
        sheet = fold(sheet, axis, pos)
    print("Dots, first fold", sheet.sum())

    # Part 2.
    for axis, pos in folds[1:]:
        sheet = fold(sheet, axis, pos)
    print("Final paper")
    pprint(sheet)
