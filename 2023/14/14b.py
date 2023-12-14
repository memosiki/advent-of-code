import itertools
from enum import IntEnum

import numpy as np
from numpy.typing import NDArray

with open("input", "r") as fd:
    matrix = [bytearray(line.rstrip(), encoding="utf-8") for line in fd]
    plate = np.array(matrix, dtype=np.uint8)
max_x, max_y = plate.shape


def deserialize(data: bytes):
    return np.array([line for line in itertools.batched(data, max_x)])


class Direction(IntEnum):
    # ordering is important
    # direction is the count of 90degrees rotations clockwise from the north position
    north = 0
    west = 1
    south = 2
    east = 3


def shift_north(field: NDArray) -> NDArray:
    """
    Lean field north and shift round rocks.
    """
    # most north available space
    M = field.shape[1]
    footing = np.zeros(M, dtype=np.int_)
    for y, line in enumerate(field):
        for x, rock in enumerate(line):
            if rock == ord(b"O"):
                field[y][x] = ord(b".")
                field[footing[x]][x] = ord(b"O")
                footing[x] += 1
            elif rock == ord(b"#"):
                footing[x] = y + 1
    return field


def calc_load(field: NDArray) -> int:
    M = field.shape[1]
    load = 0
    for y, line in enumerate(field):
        for rock in line:
            if rock == ord(b"O"):
                load += M - y
    return load


def pprint(field: NDArray):
    for line in to_char(field):
        print(*line, sep="")
    print()


to_char = np.vectorize(chr)
seen: dict[bytes, int] = {}
# pprint(plate)
plate = np.rot90(plate, 1)

time = 0
while True:
    time += 1
    plate = shift_north(np.rot90(plate, -1))
    plate = shift_north(np.rot90(plate, -1))
    plate = shift_north(np.rot90(plate, -1))
    plate = shift_north(np.rot90(plate, -1))
    frozen_plate = np.rot90(plate, -1).tobytes()

    if frozen_plate in seen:
        print("Repeat at", time)
        break
    seen[frozen_plate] = time

total_time = 1000000000
plates = {plate: time for time, plate in seen.items()}
prev = seen[frozen_plate]
total_time -= prev
cycle = time - prev
time = prev + total_time % cycle
plate = plates[time]

load = calc_load(deserialize(plate))

print("Load", load)
