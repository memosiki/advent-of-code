from collections import defaultdict

with open('input', 'r') as fd:
    pattern = fd.readline().rstrip().strip('^$')
depths: dict[complex] = defaultdict(lambda: float("inf"))
depths[0 + 0j] = 0
stack = []
position = 0 + 0j
step = {'N': -1, 'W': -1j, 'S': 1, 'E': 1j}
for char in pattern:
    match char:
        case '(':
            stack.append(position)
        case ')':
            position = stack.pop()
        case '|':
            position = stack[-1]
        case _:
            depths[position + step[char]] = min(depths[position] + 1, depths[position + step[char]])
            position += step[char]

print("Max depth:", max(depths.values()))
min_depth = 1_000
room_count = sum(depth >= min_depth for depth in depths.values())
print(f"Rooms at least {min_depth} deep:", room_count)
