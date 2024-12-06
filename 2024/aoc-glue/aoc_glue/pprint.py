import numpy as np


def pprint_spelled(arr: np.ndarray | list[list], t=False):
    if t:
        arr = np.transpose(arr)
    for row in np.vectorize(lambda x: "█" if x else "░")(arr):
        print(*row, sep="")


def pprint_matrix[T](arr: np.ndarray[T] | list[list[T]]):
    for row in arr:
        print(*row, sep="")
