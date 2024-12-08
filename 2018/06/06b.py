import sys
from copy import deepcopy
from functools import partial
from queue import Queue

from tqdm import tqdm

GRID_SIZE = 1000
MIN_PROXIMITY = 10_000
# MIN_PROXIMITY = 32
grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
visited = deepcopy(grid)

# coords of points of interests
x_interest = []
y_interest = []

for line in sys.stdin:
    x, y = map(int, line.split(", "))
    x_interest.append(x)
    y_interest.append(y)


def dist(x, y, i):
    # distance between (x,y) and i-th point of interest
    return abs(x_interest[i] - x) + abs(y_interest[i] - y)


points_of_interest = range(len(x_interest))
for x in tqdm(range(GRID_SIZE), desc="voronoi"):
    for y in range(GRID_SIZE):
        dist_curr = partial(dist, x, y)
        grid[x][y] = sum(map(dist_curr, points_of_interest)) < MIN_PROXIMITY


def DFS(x, y) -> int:
    """returns the area of the region"""
    area = 0
    if not grid[x][y]:
        return 0
    if x >= 0 and not visited[x - 1][y]:
        visited[x - 1][y] = True
        area += DFS(x - 1, y)

    if y >= 0 and not visited[x][y - 1]:
        visited[x][y - 1] = True
        area += DFS(x, y - 1)

    if x < GRID_SIZE - 1 and not visited[x + 1][y]:
        visited[x + 1][y] = True
        area += DFS(x + 1, y)

    if y < GRID_SIZE - 1 and not visited[x][y + 1]:
        visited[x][y + 1] = True
        area += DFS(x, y + 1)
    return area


def BFS(x, y) -> int:
    visited[x][y] = True
    queue = Queue()
    queue.put((x, y))
    area = 0
    while not queue.empty():
        (x, y) = queue.get()
        if grid[x][y]:
            area += 1
        if x >= 0 and not visited[x - 1][y]:
            visited[x - 1][y] = True
            queue.put((x - 1, y))
        if y >= 0 and not visited[x][y - 1]:
            visited[x][y - 1] = True
            queue.put((x, y - 1))
        if x < GRID_SIZE - 1 and not visited[x + 1][y]:
            visited[x + 1][y] = True
            queue.put((x + 1, y))
        if y < GRID_SIZE - 1 and not visited[x][y + 1]:
            visited[x][y + 1] = True
            queue.put((x, y + 1))
    return area


area = 0
for x in tqdm(range(GRID_SIZE), desc="bfs"):
    for y in range(GRID_SIZE):
        area = max(area, BFS(x, y))
print(area)
