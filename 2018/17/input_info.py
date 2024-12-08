import sys

from aoc_glue.input import parse_ints

X = []
Y = []
for line in sys.stdin:
    if line[0] == "x":
        (x, y1, y2) = parse_ints(line)
        X.append(x)
        Y.extend((y1, y2))
    else:
        (y, x1, x2) = parse_ints(line)
        Y.append(y)
        X.extend((x1, x2))

print("x", min(X), max(X))
print("y", min(Y), max(Y))
