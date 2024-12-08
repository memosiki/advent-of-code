import string
import sys
from collections import Counter

from tqdm import tqdm

GRID_SIZE = 1000
NOT_FILLED = -1
MULTIPLE_CLOSEST = -2
grid = [[NOT_FILLED] * GRID_SIZE for _ in range(GRID_SIZE)]

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
for x in tqdm(range(GRID_SIZE)):
    # for y in tqdm(range(GRID_SIZE), desc="y", position=1):
    for y in range(GRID_SIZE):
        min_dist = (GRID_SIZE + 1) ** 2
        closest_poi = NOT_FILLED
        count = 0
        for poi in points_of_interest:
            if dist(x, y, poi) < min_dist:
                min_dist = dist(x, y, poi)
                closest_poi = poi
                count = 1
            elif dist(x, y, poi) == min_dist:
                count += 1
        grid[x][y] = MULTIPLE_CLOSEST if count > 1 else closest_poi
boundless = set()
n = GRID_SIZE - 1
for i in range(GRID_SIZE):
    boundless.add(grid[0][i])
    boundless.add(grid[n][i])
    boundless.add(grid[i][0])
    boundless.add(grid[i][n])

areas: Counter = sum((Counter(line) for line in grid), start=Counter())
assert areas[NOT_FILLED] == 0

boundless.add(MULTIPLE_CLOSEST)
for poi_id in boundless:
    areas.pop(poi_id)

poi_id, area = areas.most_common(1)[0]


def transpose_grid():
    for i in range(GRID_SIZE):
        for j in range(i):
            grid[i][j], grid[j][i] = grid[j][i], grid[i][j]


def print_grid():
    transpose_grid()  # match the example

    mapping = {MULTIPLE_CLOSEST: ".", NOT_FILLED: "!"} | {
        i: char for i, char in zip(points_of_interest, string.ascii_lowercase)
    }
    bb = 10  # bounding box
    for line in grid[:bb]:
        print(*map(mapping.get, line[:bb]), sep="")


# print_grid()

print(poi_id)
print(area)  # answer
