import math

EPS = 1e-4
answer = 1
times = map(int, input().split(":")[1].split())
distances = map(int, input().split(":")[1].split())

"""
x*(t-x) >= dist
x^2 - xt + dist <= 0
"""

for t, d in zip(times, distances):

    def is_root(x) -> bool:
        return -EPS <= x**2 - t * x + d <= EPS

    # assume equation has two roots
    lbound = math.ceil((t - math.sqrt(t**2 - 4 * d)) * 0.5)
    rbound = math.floor((t + math.sqrt(t**2 - 4 * d)) * 0.5)
    if is_root(lbound):
        lbound += 1
    if is_root(rbound):
        rbound -= 1
    answer *= rbound - lbound + 1

print(answer)
