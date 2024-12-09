import random

N = 7
assert N % 2, "N must be odd"

print(*random.choices(list(range(10)), k=N), sep="")
