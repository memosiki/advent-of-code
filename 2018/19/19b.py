reg2 = 10551287  # reg[2] is constant
reg0 = 0
for reg3 in range(1, reg2 + 1):
    if reg2 % reg3 == 0:  # reg5 * reg3 == reg2
        reg0 += reg3
print(f"{reg0=}")
