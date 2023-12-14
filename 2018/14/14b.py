import math

from tqdm import tqdm

pattern = 323081
digits = math.floor(math.log(pattern, 10)) + 1
order = 10 ** (digits - 1)
MAX_ITERATIONS = order**2

recipies = [3, 7]
a, b = 3, 7
posa, posb = 0, 1


def shift_check(curr, lowest, count) -> int:
    curr = (curr % order) * 10 + lowest
    if curr == pattern:
        print("Found", count - digits)
        exit(0)
    return curr


curr = 0
for i in tqdm(range(MAX_ITERATIONS)):
    if a + b >= 10:
        recipies.append(1)
        curr = shift_check(curr, 1, len(recipies))
        recipies.append(a + b - 10)
        curr = shift_check(curr, a + b - 10, len(recipies))
    else:
        recipies.append(a + b)
        curr = shift_check(curr, a + b, len(recipies))
    posa = (posa + a + 1) % len(recipies)
    posb = (posb + b + 1) % len(recipies)
    a = recipies[posa]
    b = recipies[posb]
print("Failed")
