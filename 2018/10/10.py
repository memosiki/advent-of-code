import re
import sys
from collections import Counter
from copy import deepcopy

from tqdm import tqdm

pattern = re.compile(r"(-?\d+)")
x = []
y = []
vx = []
vy = []

for line in sys.stdin:
    [x_i, y_i, vx_i, vy_i] = map(int, pattern.findall(line))
    x.append(x_i)
    y.append(y_i)
    vx.append(vx_i)
    vy.append(vy_i)

count = len(x)
CONSTELLATION_TIME = 10_345  # empirical result
time_start = CONSTELLATION_TIME
time_end = CONSTELLATION_TIME + 1
BOUNDING_BOX = 200
HALF_BB = BOUNDING_BOX // 2
BRUSH = "#"
offset_x = -100
offset_y = -100
screen = [["."] * BOUNDING_BOX for _ in range(BOUNDING_BOX)]
clear_screen = deepcopy(screen)

varmin, tmin = float("inf"), 0
for time in tqdm(range(time_start, time_end)):
    xvar = len(Counter(x[i] + vx[i] * time for i in range(count)))
    yvar = len(Counter(y[i] + vy[i] * time for i in range(count)))
    var = min(xvar, yvar)
    if var < varmin:
        tmin = time
        varmin = var

print("Probably at:", tmin, varmin)
# exit(0)
for time in range(time_start, time_end):
    skip = False
    screen = deepcopy(clear_screen)
    for i in range(count):
        yi, xi = offset_y + y[i] + vy[i] * time, offset_x + x[i] + vx[i] * time
        if 0 <= xi <= BOUNDING_BOX and 0 <= yi <= BOUNDING_BOX:
            screen[yi][xi] = BRUSH
        else:
            print("Outside bb:", yi, xi)
            skip = True
            break
    if skip:
        continue
    # print(time, "—" * BOUNDING_BOX)
    for line in screen:
        print(*line)
