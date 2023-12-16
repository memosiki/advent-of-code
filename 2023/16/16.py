from enum import StrEnum
from queue import Queue
from typing import Final

import numpy as np
from tqdm import tqdm

from aoc_glue.input import parse_matrix

with open("input", "r") as fd:
    field: Final = np.array(parse_matrix(fd))


class Dir(StrEnum):
    up = "^"
    left = "<"
    right = ">"
    down = "v"

    @staticmethod
    def split(x, y):
        return {
            "|": ((x, y - 1, Dir.up), (x, y + 1, Dir.down)),
            "-": ((x + 1, y, Dir.right), (x - 1, y, Dir.left)),
        }[field[y][x]]

    def move(self, x, y):
        return {
            ">": (x + 1, y),
            "<": (x - 1, y),
            "v": (x, y + 1),
            "^": (x, y - 1),
        }[self]

    def splitting(self, splitter) -> bool:
        return self in {"|": (">", "<"), "-": ("v", "^")}.get(splitter, ())

    def turn(self, mirror):
        return Dir(
            {
                ("/", "v"): "<",
                ("/", ">"): "^",
                ("/", "^"): ">",
                ("/", "<"): "v",
                ("\\", "v"): ">",
                ("\\", "<"): "^",
                ("\\", ">"): "v",
                ("\\", "^"): "<",
            }.get((mirror, self), self)
        )

    def to_int(self) -> int:
        return {">": 0, "v": 1, "<": 2, "^": 3}[self]


N, M = field.shape
assert N == M


def inbounds(x, y):
    return 0 <= x < N and 0 <= y < N


def energize(start_x, start_y, start_dir):
    visited = np.zeros((4,) + field.shape, dtype=np.bool_)

    def visit(x, y, dir):
        if inbounds(x, y):
            res = visited[dir.to_int(), y, x]
            visited[dir.to_int(), y, x] = True
            return res
        return True

    queue = Queue()
    queue.put((start_x, start_y, start_dir))
    visit(start_x, start_y, start_dir)
    while not queue.empty():
        x, y, dir = queue.get()
        if dir.splitting(field[y][x]):
            beam1, beam2 = Dir.split(x, y)
            if not visit(*beam1):
                queue.put(beam1)
            if not visit(*beam2):
                queue.put(beam2)
            continue
        dir = dir.turn(field[y][x])
        x, y = dir.move(x, y)
        if not visit(x, y, dir):
            queue.put((x, y, dir))

    visited = np.add.reduce(visited) > 0
    return np.sum(np.sum(visited))


max_energy = 0
for i in tqdm(range(N)):
    max_energy = max(
        max_energy,
        energize(0, i, Dir.right),
        energize(N - 1, i, Dir.left),
        energize(i, 0, Dir.down),
        energize(i, N - 1, Dir.up),
    )
print("Energy at 0, 0:", energize(0, 0, Dir.right))
print("Max energized", max_energy)
