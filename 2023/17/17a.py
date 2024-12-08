from queue import PriorityQueue

import numpy as np

with open("input", "r") as fd:
    field = np.array([list(map(int, line.rstrip())) for line in fd])


# Enum is too clumsy
# up = 0
# left = 1
# down = 2
# right = 3


def move(dir, x, y):
    return {0: (x, y - 1), 1: (x - 1, y), 2: (x, y + 1), 3: (x + 1, y)}[dir]


print(field)
turns = {0: (0, 1, 3), 1: (0, 1, 2), 2: (1, 2, 3), 3: (0, 2, 3)}
(N, M) = field.shape
# assert N == M
# 4 additional dimensions for direction and 0...3 for consecutive steps in that direction
visited = np.full((*field.shape, 4, 4), np.inf)
target = (N - 1, M - 1)
# Dijkstra
pq = PriorityQueue()
pq.put((0, 0, 0, 1, 0))
pq.put((0, 0, 0, 2, 0))
while not pq.empty():
    heat0, x0, y0, dir0, step0 = pq.get()
    if (x0, y0) == target:
        break
    for dir in turns[dir0]:
        x, y = move(dir, x0, y0)
        if 0 <= x < N and 0 <= y < M:
            heat = heat0 + field[x][y]
            start_step = step0 + 1 if dir == dir0 else 1
            for step in range(start_step, 4):
                if heat < visited[x][y][dir][step]:
                    visited[x][y][dir][step] = heat
                    pq.put((heat, x, y, dir, start_step))
print("Minimal heat loss", visited[target].min())
