import numpy as np
from aoc_glue.input import parse_matrix

with open("input", "r") as f:
    plate = np.array(parse_matrix(f))
max_x, max_y = plate.shape
# most north available space
footing = np.zeros(plate.shape[0], dtype=np.int_)
load = 0
for y, line in enumerate(plate):
    for x, rock in enumerate(line):
        if rock == "O":
            load += max_y - footing[x]
            footing[x] += 1
        elif rock == "#":
            footing[x] = y + 1

print("Load", load)
