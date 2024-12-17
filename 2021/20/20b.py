from itertools import product

import numpy as np
from aoc_glue.input import parse_np_matrix
from aoc_glue.pprint import pprint_spelled
from bitarray import bitarray
from tqdm import tqdm

# Part 1. steps =2
# Part 2. steps =50
STEPS = 50

PAD = (
    STEPS + 1
)  # image grows at most 1 layer at the border with each step, +1 for actual padding
MASK_LEN = 9
FLIPMASK = (1 << MASK_LEN) - 1

if __name__ == "__main__":
    # Parsing
    program = bitarray(char == "#" for char in input())
    input()
    assert len(program) == 1 << MASK_LEN
    assert not (STEPS % 2), "Only works for even steps"
    image = parse_np_matrix(dtype=np.str_).T
    image: np.ndarray = image == "#"
    image = np.pad(image, PAD, constant_values=False)
    N, M = image.shape

    # todo: use bitarray for image
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

    # flipping image to negative each step since bright for program[0] is alternating colors
    mask = 0b000000000
    is_flipping = not program[0]
    for step in tqdm(range(1, STEPS + 1)):
        odd = step % 2
        mask = FLIPMASK * (not odd)
        new_image = np.full_like(image, is_flipping and odd, dtype=np.bool_)
        for x, y in product(range(1, N - 1), range(1, M - 1)):
            new_image[x, y] = program[filter(x, y, image) ^ mask] ^ odd
        image = new_image

    print("Final image")
    pprint_spelled(image)
    print("Total lit", image.sum())
