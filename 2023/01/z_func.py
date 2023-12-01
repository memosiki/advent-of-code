line = input()
Z = [0] * len(line)
n = len(line)

# == Trivial implementation ==

for i in range(n):
    # undetermined for index 0
    if i == 0:
        Z[0] = -1
        continue
    overlap = 0
    while i + overlap < n and line[overlap] == line[i + overlap]:
        overlap += 1
    Z[i] = overlap

