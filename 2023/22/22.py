from sortedcontainers import SortedList

from aoc_glue.input import parse_ints

bricks = []
with open("input", "r") as fd:
    for line in fd:
        # x1, y1, z1, x2, y2, z2
        bricks.append(tuple(parse_ints(line)))
bricks.sort(key=lambda x: (x[2], x[5]))


def intersects(i, j):
    xa1, ya1, _, xa2, ya2, _ = bricks[i]
    xb1, yb1, _, xb2, yb2, _ = bricks[j]
    return max(xa1, xb1) <= min(xa2, xb2) and max(ya1, yb1) <= min(ya2, yb2)


# Blocks that support the current piece in place
foundation = [[] for _ in range(len(bricks))]
# Blocks supported by the current piece
supports = [[] for _ in range(len(bricks))]
# Final z coordinate in the tower after settling the fall
final_z = [-1 for _ in range(len(bricks))]

# Z-maps for upper and lower edges of bricks
z_list = SortedList()
bottom_z_list = SortedList()

# Try to lower the piece until it is intercepted and track all of such blocks
for i in range(len(bricks)):
    z_match = 0
    _, _, za1, _, _, za2 = bricks[i]
    for z, j in reversed(z_list):
        if z < z_match:
            break
        if intersects(i, j):
            foundation[i].append(j)
            supports[j].append(i)
            z_match = z
    z_list.add((z_match + 1 + (za2 - za1), i))
    bottom_z_list.add((z_match + 1, i))
    final_z[i] = z_match + 1
# print(supported_by)
# print(supports)

# Part 1
# Any block that supports other blocks that are exclusively supported
# by the only one block cannot be removed
can_be_removed = 0
for blocks in supports:
    can_be_removed += all(len(foundation[id]) > 1 for id in blocks)

# Part 2
# Try to remove any block and collapse subsequent ones in lower edge z_list order
total_fall = 0
for i in range(len(bricks)):
    fallen = [False] * len(bricks)
    fallen[i] = True
    starting_z = bottom_z_list.bisect_left((final_z[i], -1))
    for _, j in bottom_z_list[starting_z:]:
        if i == j:
            continue
        # has a foundation and all of it has collapsed
        fallen[j] = bool(foundation[j]) and all(fallen[k] for k in foundation[j])
    # -1 for the initial disintegrated piece
    total_fall += sum(fallen) - 1

print("Can be removed", can_be_removed)
print("Total pieces that fall", total_fall)
