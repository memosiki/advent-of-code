from aoc_glue.input import parse_ints

points = []
with open("input", "r") as fd:
    for line in fd:
        x, y, z, w = parse_ints(line)
        points.append((x, y, z, w))


def dist(pointa, pointb):
    xa, ya, za, wa = pointa
    xb, yb, zb, wb = pointb
    return abs(xa - xb) + abs(ya - yb) + abs(za - zb) + abs(wa - wb)


N = len(points)
graph: dict[int, list[int]] = {i: [] for i in range(N)}
CONSTELLATION_DIST = 3
for i in range(N):
    for j in range(i + 1, N):
        if dist(points[i], points[j]) <= CONSTELLATION_DIST:
            graph[i].append(j)
            graph[j].append(i)

print(graph)
# DFS for components
visited = [False] * N


def dfs(node):
    for child in graph[node]:
        if not visited[child]:
            visited[child] = True
            dfs(child)


components = 0
for i in range(N):
    if not visited[i]:
        visited[i] = True
        components += 1
        dfs(i)

# Complexity O(n^2)
print("Constellations", components)
