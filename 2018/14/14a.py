from tqdm import tqdm

iterations = 0
OFFSET = 10

recipies = [3, 7]
a, b = 3, 7
posa, posb = 0, 1
for i in tqdm(range(iterations + OFFSET)):
    if a + b >= 10:
        recipies.append(1)
        recipies.append(a + b - 10)
    else:
        recipies.append(a + b)
    posa = (posa + a + 1) % len(recipies)
    posb = (posb + b + 1) % len(recipies)
    a = recipies[posa]
    b = recipies[posb]

answer = recipies[iterations : iterations + OFFSET]
print("".join(str(digit) for digit in answer))
