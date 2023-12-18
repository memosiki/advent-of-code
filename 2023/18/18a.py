def move(dir, step, x, y):
    return {
        "U": (x, y - step),
        "D": (x, y + step),
        "L": (x - step, y),
        "R": (x + step, y),
    }[dir]


x = y = 0
interior_area = 0
border_area = 0
with open("input", "r") as fd:
    for line in fd:
        dir, step, *_ = line.split()
        step = int(step)
        x1, y1 = move(dir, step, x, y)
        # shoelace formulae
        # interior_area += (y1 + y) * (x - x1)
        interior_area += x * y1 - x1 * y
        x, y = x1, y1
        border_area += step
# assert contour is enclosed
assert (x, y) == (0, 0)
assert border_area % 2 == 0
assert interior_area % 2 == 0

interior_area = abs(interior_area) // 2
# pick's theorem
# a = i + b/2 - 1
# i = a - b/2 + 1
interior_points = interior_area - border_area // 2 + 1
total_area = interior_points + border_area
print("Total area", total_area)
