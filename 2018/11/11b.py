from tqdm import tqdm

serial = 1308
RACK_SIZE = 300
rack = [[0] * RACK_SIZE for _ in range(RACK_SIZE)]


def power_lvl(x, y):
    x, y = x + 1, y + 1
    return ((x + 10) * y + serial) * (x + 10) // 100 % 10 - 5


for x in range(RACK_SIZE):
    for y in range(RACK_SIZE):
        # cell power level
        rack[y][x] = power_lvl(x, y)

max_power = float("-inf")
xmax, ymax, pattern_max = 0, 0, 0

# O(N^5), where N=300, so O(1) ( /._.)
for pattern in tqdm(range(RACK_SIZE + 1)):
    for x in range(RACK_SIZE - pattern):
        for y in range(RACK_SIZE - pattern):
            power = sum(sum(rack[yi][x : x + pattern]) for yi in range(y, y + pattern))
            max_power, xmax, ymax, pattern_max = max(
                (max_power, xmax, ymax, pattern_max), (power, x, y, pattern)
            )
print(xmax + 1, ymax + 1, pattern_max, sep=",")
