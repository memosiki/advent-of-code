import re
import sys

PLANE_SIZE = 1000
plane = [[0] * PLANE_SIZE for _ in range(PLANE_SIZE)]
pattern = re.compile(R"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
for line in sys.stdin:
    match = re.search(pattern, line)
    _, L, U, W, H = map(int, match.groups())
    for i in range(L, L + W):
        for j in range(U, U + H):
            plane[i][j] += 1

answer = sum(sum(map(lambda x: x > 1, line)) for line in plane)
print(answer)
