import itertools

import numpy as np
from aoc_glue.input import parse_np_matrix
from tqdm import tqdm

if __name__ == "__main__":
    field = parse_np_matrix(dtype=str)
    N, M = field.shape
    next_field = field.copy()
    for step in tqdm(itertools.count(start=1), disable=False):
        moves = 0

        field = next_field
        next_field = field.copy()
        eastward = np.where(field == ">")
        for x, y in zip(*eastward):
            if field[x, (y + 1) % M] == ".":
                moves += 1
                next_field[x, y] = "."
                next_field[x, (y + 1) % M] = ">"

        field = next_field
        next_field = field.copy()
        southward = np.where(field == "v")
        for x, y in zip(*southward):
            if field[(x + 1) % N, y] == ".":
                moves += 1
                next_field[x, y] = "."
                next_field[(x + 1) % N, y] = "v"
        if not moves:
            break
    print("Step", step)
