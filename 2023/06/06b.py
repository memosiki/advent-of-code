import math

EPS = 1e-4
time = int("".join(input().split(":")[1].split()))
distance = int("".join(input().split(":")[1].split()))

"""
x*(t-x) >= dist
x^2 - xt + dist <= 0
"""


def is_root(x) -> bool:
    return -EPS <= x ** 2 - time * x + distance <= EPS


lbound = math.ceil((time - math.sqrt(time ** 2 - 4 * distance)) * 0.5)
print((time - math.sqrt(time ** 2 - 4 * distance)) * 0.5)
rbound = math.floor((time + math.sqrt(time ** 2 - 4 * distance)) * 0.5)
print((time + math.sqrt(time ** 2 - 4 * distance)) * 0.5)
if is_root(lbound):
    lbound += 1
if is_root(rbound):
    rbound -= 1
answer = rbound - lbound + 1
print(answer)
