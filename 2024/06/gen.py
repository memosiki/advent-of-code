from random import choices

N = 40
GUARANTEE_SOLVABLE = False
field = []
for _ in range(N):
    field.append(list(choices([".", "#"], [0.9, 0.1], k=N)))

start_x = N // 2
start_y = N // 2
field[start_y][start_x] = "^"

if GUARANTEE_SOLVABLE:
    for y in range(start_y):
        field[y][start_x] = "."


for i in range(N):
    print(*field[i], sep="")
