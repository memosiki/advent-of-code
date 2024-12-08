from enum import IntEnum
from queue import PriorityQueue
from typing import Final

import numpy as np
from tqdm import tqdm

MOD: Final = 20183

# input
depth = 7305
target = (13, 734)

# example data
# depth = 510
# target = (10, 10)

# calculate the area with coords larger than target
padding = 1000

target_x, target_y = target
max_x, max_y = target_x + padding + 1, target_y + padding + 1
geological = np.zeros((max_x, max_y), dtype="int64")
erosion = np.zeros((max_x, max_y), dtype="int64")
for i in range(1, max_x):
    geological[i][0] = 16807 * i
    erosion[i][0] = (geological[i][0] + depth) % MOD

for i in range(1, max_y):
    geological[0][i] = 48271 * i
    erosion[0][i] = (geological[0][i] + depth) % MOD

for x in range(1, max_x):
    for y in range(1, max_y):
        geological[x][y] = (erosion[x - 1][y] * erosion[x][y - 1]) % MOD
        erosion[x][y] = (geological[x][y] + depth) % MOD

erosion[target_x][target_y] = 0

to_char = np.vectorize(lambda x: {0: ".", 1: "=", 2: "|"}[x])
cave = erosion % 3
# print(to_char(cave.T))
print("Total risk level", cave[: target_x + 1, : target_y + 1].sum())


def heuristic(x1, y1):
    return 7 * abs(x1 - target_x) + 7 * abs(y1 - target_y)


class Region(IntEnum):
    rocky = 0
    wet = 1
    narrow = 2


class Equip(IntEnum):
    torch = 0
    climbing = 1
    neither = 2


allowed = {
    Region.rocky: {Equip.torch, Equip.climbing},
    Region.wet: {Equip.climbing, Equip.neither},
    Region.narrow: {Equip.neither, Equip.torch},
}

# Dijkstra
# A* can't converge for some reason
pq = PriorityQueue()
depths = np.full((*cave.shape, len(Equip)), np.inf)
start = (0, 0)
pq.put((0, Equip.torch, start))
depths[0][0][Equip.torch] = 0
progress = tqdm(ascii=True)
while not pq.empty():
    _, equip, (x, y) = pq.get()
    # assert depth == depths[x][y][equip]
    if (x, y) == target:
        break
    region = cave[x][y]
    for xi, yi in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if xi < 0 or yi < 0:
            continue
        for equip_i in allowed[cave[x][y]] & allowed[cave[xi][yi]]:
            depth_i = depths[x][y][equip] + 1 + 7 * (equip_i != equip)
            if depth_i < depths[xi][yi][equip_i]:
                depths[xi][yi][equip_i] = depth_i
                pq.put((depth_i, equip_i, (xi, yi)))
    progress.update()

min_time = min(
    depths[target_x][target_y][Equip.torch],
    depths[target_x][target_y][Equip.climbing] + 7,
    depths[target_x][target_y][Equip.neither] + 7,
)
print("Minimal time", min_time)
