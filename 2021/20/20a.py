from itertools import product

import numpy as np
from aoc_glue.input import parse_np_matrix
from aoc_glue.pprint import pprint_spelled
from bitarray import bitarray

STEPS = 2
PAD = 2 * STEPS
if __name__ == "__main__":
    # Parsing
    program = bitarray(char == "#" for char in input())
    input()
    assert len(program) == 1 << 9
    image = parse_np_matrix(dtype=np.str_).T
    image: np.ndarray = image == "#"
    image = np.pad(image, PAD, constant_values=False)
    N, M = image.shape

    def filter(x0: int, y0: int, image: np.ndarray) -> int:
        idx = 0
        for offset, (x, y) in enumerate(
            (
                (x0 + 1, y0 + 1),
                (x0, y0 + 1),
                (x0 - 1, y0 + 1),
                (x0 + 1, y0),
                (x0, y0),
                (x0 - 1, y0),
                (x0 + 1, y0 - 1),
                (x0, y0 - 1),
                (x0 - 1, y0 - 1),
            )
        ):
            idx |= image[x, y] << offset
        return idx

    for step in range(1, STEPS + 1):
        # every step shrinks padded border by 1, since the all-dark pixels translate to all-bright
        new_image = np.zeros_like(image, dtype=np.bool_)
        for x, y in product(range(step, N - step), range(step, M - step)):
            new_image[x, y] = program[filter(x, y, image)]
        image = new_image
    print("Final image")
    pprint_spelled(image)
    print("Total lit", image.sum())
