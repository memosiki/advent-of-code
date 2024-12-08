import sys

import numpy as np

if __name__ == "__main__":
    LOOKUP = "XMAS"
    total = 0
    row = input()
    field = np.array(tuple(row), dtype=np.dtypes.StringDType)
    for row in sys.stdin:
        field = np.vstack((field, tuple(row.strip())))

    # rows
    for i in range(field.shape[0]):
        total += "".join(field[i, :]).count(LOOKUP)
        total += "".join(field[i, ::-1]).count(LOOKUP)
    # columns
    for i in range(field.shape[1]):
        total += "".join(field[:, i]).count(LOOKUP)
        total += "".join(field[::-1, i]).count(LOOKUP)
    # diagonals
    inv_field = np.fliplr(field)
    for i in range(-field.shape[0] + 1, field.shape[1]):
        # main
        total += "".join(field.diagonal(i)).count(LOOKUP)
        total += "".join(field.diagonal(i)[::-1]).count(LOOKUP)
        # secondary
        total += "".join(inv_field.diagonal(i)).count(LOOKUP)
        total += "".join(inv_field.diagonal(i)[::-1]).count(LOOKUP)

    print("Count", LOOKUP, total)
