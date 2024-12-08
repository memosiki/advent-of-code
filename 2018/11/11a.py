serial = 1308
RACK_SIZE = 300
PATTERN_SIZE = 3
rack = [[0] * RACK_SIZE for _ in range(RACK_SIZE)]


def power_lvl(x, y):
    x, y = x + 1, y + 1
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


def debug_preview():
    preview_x = 20
    preview_y = 60
    preview_x, preview_y = preview_x - 1, preview_y - 1
    offset = 5
    for line in rack[preview_y : preview_y + offset]:
        print("".join(f"{num:>3}" for num in line[preview_x : preview_x + offset]))


# == Solution==

for x in range(RACK_SIZE):
    for y in range(RACK_SIZE):
        # cell power level
        rack[y][x] = power_lvl(x, y)

max_power = float("-inf")
xmax, ymax = 0, 0
for x in range(RACK_SIZE - PATTERN_SIZE):
    for y in range(RACK_SIZE - PATTERN_SIZE):
        power = sum(
            sum(rack[yi][x : x + PATTERN_SIZE]) for yi in range(y, y + PATTERN_SIZE)
        )
        if power > max_power:
            xmax, ymax = x, y
            max_power = power
print(xmax + 1, ymax + 1, sep=",")
