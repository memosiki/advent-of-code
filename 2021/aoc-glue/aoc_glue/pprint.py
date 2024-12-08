import numpy as np


def pprint_spelled(arr: np.ndarray):
    for row in np.vectorize(lambda x: "█" if x else "░")(np.transpose(arr)):
        print(*row, sep="")


def pprint_matrix[T](arr: np.ndarray[T] | list[list[T]]):
    for row in arr:
        print(*row, sep="")
