import re
import sys

PLANE_SIZE = 1000
plane = [[0] * PLANE_SIZE for _ in range(PLANE_SIZE)]
overlapped = set()
claims = set()
pattern = re.compile(R"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
for line in sys.stdin:
    match = re.search(pattern, line)
    claim_id, L, U, W, H = map(int, match.groups())
    claims.add(claim_id)
    for i in range(L, L + W):
        for j in range(U, U + H):
            if plane[i][j]:
                overlapped.add(plane[i][j])
                overlapped.add(claim_id)
            plane[i][j] = claim_id

answer = claims - overlapped
assert len(answer) == 1
print(answer.pop())
