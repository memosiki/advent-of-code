import math

from tqdm import tqdm

"""
(r2 + 1) * 256 > r5
r2 > r5/256 - 1

r2[i] > r2[i-1]/256 - 1    <=>  ceil + %==0
"""

reg2 = 65536
reg4 = 9138982
print(f"{reg2:<10} {reg4:<10}")

seen: dict[int, int] = {}
time = 0
for x in tqdm(range(16777215), ascii=True):
    time += 1
    if 256 > reg2:
        reg2 = reg4 | 65536
        reg4 = 10704114
    else:
        reg2 = math.ceil(reg2 / 256 - 1) + (reg2 % 256 == 0)
    reg4 += reg2 & 255
    reg4 &= 16777215
    reg4 *= 65899
    reg4 &= 16777215
    # print(f"{reg2:<10} {reg4:<10}")
    if reg4 not in seen:
        seen[reg4] = time

print("Latest halt at reg[0]", max(seen, key=seen.get))
