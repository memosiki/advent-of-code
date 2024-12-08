offsets = {"U": -1j, "D": 1j, "L": -1, "R": 1}
pos = 0 + 0j
border: set[complex] = {pos}
with open("input", "r") as fd:
    for line in fd:
        dir, steps, _ = line.split()
        for _ in range(int(steps)):
            pos += offsets[dir]
            border.add(pos)
corner = sorted(list(border), key=lambda x: (x.real, x.imag))[0]
# dfs
start = corner + 1 + 1j
visited = {node: True for node in border}

print(start, border)
stack = [start]
while stack:
    node = stack.pop()
    for offset in offsets.values():
        if node + offset not in visited:
            visited[node + offset] = True
            stack.append(node + offset)
print("Area:", len(visited))
