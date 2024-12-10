from functools import cache
from itertools import product

from aoc_glue.input import parse_np_matrix

PEAK = 9
START = 0
if __name__ == "__main__":
    field = parse_np_matrix()
    N, M = field.shape

    # O(N) time, 0(N) space
    @cache
    def traverse(x0, y0) -> set[tuple[int, int]]:
        if field[x0, y0] >= PEAK:
            return {(x0, y0)}
        peaks = frozenset()
        for x, y in (
            (x0 - 1, y0),
            (x0 + 1, y0),
            (x0, y0 - 1),
            (x0, y0 + 1),
        ):
            if 0 <= x < M and 0 <= y < N and field[x, y] == field[x0, y0] + 1:
                peaks = {*peaks, *traverse(x, y)}
        return peaks

    score = 0
    for x0, y0 in product(range(M), range(N)):
        if field[x0, y0] == START:
            peaks = traverse(x0, y0)
            score += len(peaks)
            # print("From", x0, y0, "to", peaks)
    print("Score", score)
