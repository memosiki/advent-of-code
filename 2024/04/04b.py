import sys

import numpy as np


def findall(needle, haystack):
    # find non-intersecting occurrences of needle in haystack, 0(n*m)
    i = haystack.find(needle)
    while i != -1:
        yield i
        i = haystack.find(needle, i + 1)


if __name__ == "__main__":
    row = input()
    field = np.array(tuple(row), dtype=np.dtypes.StringDType)
    for row in sys.stdin:
        field = np.vstack((field, tuple(row.strip())))

    n, m = field.shape  # row, column
    inv_field = np.fliplr(field)

    main_locations = set()
    secondary_locations = set()

    for k in range(-n + 1, m):
        # find all occurrences of searchwords on the diagonals,
        # locations represent the center of the word
        main_diag = "".join(field.diagonal(k))
        scnd_diag = "".join(inv_field.diagonal(k))
        for searchword in ("MAS", "SAM"):
            for pos in findall(searchword, main_diag):
                main_locations.add(
                    (pos - k * (k < 0) + 1, pos + k * (k > 0) + 1),
                )
            for pos in findall(searchword, scnd_diag):
                secondary_locations.add(
                    (pos - k * (k < 0) + 1, m - 1 - pos - k * (k > 0) - 1),
                )
    total = sum(1 for pos in main_locations if pos in secondary_locations)
    print("MAS crosses", total)
