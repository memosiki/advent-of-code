# line = input()
from typing import List


# == Trivial implementation ==
def z_func_trivial(line: str) -> List[int]:
    n = len(line)
    Z = [0] * n

    # undetermined for index 0
    Z[0] = -1
    for i in range(1, n):
        overlap = 0
        while i + overlap < n and line[overlap] == line[i + overlap]:
            overlap += 1
        Z[i] = overlap
    return Z


# == O(N) ==
def z_func(line: str) -> List[int]:
    n = len(line)
    Z = [0] * n

    # Z-block: prefix with the most right border so far
    L, R = 0, 0

    # undefined for index 0
    Z[0] = -1
    for i in range(1, n):
        # inside Z-block
        if i < R:
            # fully inside Z-block
            if i + Z[i - L] < R:
                Z[i] = Z[i - L]
            else:
                """
                It is known that
                i + Z[i] > R
                so the first symbol checked is R
                """
                R = Z[i] + i
                while R < n and line[Z[i]] == line[R]:
                    R += 1
                    Z[i] += 1
                L = i
        else:
            # Trivial comparison
            Z[i] = 0
            R = Z[i] + i
            while R < n and line[Z[i]] == line[R]:
                R += 1
                Z[i] += 1
            L = i
    return Z
