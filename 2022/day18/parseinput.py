max_coord = 0
min_coord = 0
with open('input') as f:
    for line in f.readlines():
        x, y, z = list(map(int, line.split(',')))
        max_coord = max(x, y, z, max_coord)
        min_coord = min(x, y, z, min_coord)
print(max_coord, min_coord)