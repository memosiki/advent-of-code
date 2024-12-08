import itertools
from contextlib import contextmanager
from itertools import product
from typing import Collection

import numpy as np
from aoc_glue.input import parse_np_matrix
from aoc_glue.pprint import pprint_matrix
from tqdm import tqdm

type Dir = int
"""
Movement direction
    U
   L.R
    D
Vertex direction
    L
   U#D
    R
vertical = x
horizontal = y
"""
L: Dir = 0b1100
R: Dir = 0b0100
U: Dir = 0b0011
D: Dir = 0b0001
XSTEP = {
    L: 0,
    R: 0,
    U: -1,
    D: 1,
}
YSTEP = {
    L: -1,
    R: 1,
    U: 0,
    D: 0,
}

ROT = {
    U: R,
    R: D,
    D: L,
    L: U,
}
MAP = {
    U: "^",
    D: "v",
    L: "<",
    R: ">",
    0: "?",
}
type Ray = (int, int, Dir)
OOB: Ray = (-1, -1, 0)  # terminal escaping vertice


def pprint(field, graph, newob=None):
    canvas = np.empty_like(field, dtype=np.str_)
    for x, y in product(range(field.shape[0]), range(field.shape[1])):
        if field[x, y]:
            canvas[x, y] = "#"
        else:
            canvas[x, y] = "."
    for v in graph:
        if v is OOB:
            continue
        x, y, dir = v
        if canvas[x, y] != ".":
            canvas[x, y] = "+"
        else:
            canvas[x, y] = MAP[dir]
    if newob:
        canvas[newob] = "O"
    pprint_matrix(canvas)
    print()


def raycast(vertex: Ray, field, vertices: Collection[Ray]) -> Ray:
    # find downstream vertex
    x, y, dir = vertex
    rot = ROT[dir]
    # if inbounds and does not intersect boulder
    while 0 <= x < N and 0 <= y < M and not field[x, y]:
        if (x, y, rot) in vertices:
            return x, y, rot
        x += XSTEP[dir]
        y += YSTEP[dir]
    else:
        # no connecting vertices
        return OOB


def inv_raycast(vertex: Ray, field, vertices: Collection[Ray]):
    # find all upstream vertices
    x, y, dir = vertex
    rot = ROT[ROT[dir]]

    while 0 <= x < N and 0 <= y < M and not field[x, y]:
        if (x, y, rot) in vertices:
            yield x, y, rot
        x += XSTEP[dir]
        y += YSTEP[dir]


def detect_cycle(graph: dict[Ray, Ray], start: Ray) -> Ray:
    visited = set()
    node = start
    while node not in visited:
        visited.add(node)
        node = graph[node]
    return node is not OOB


@contextmanager
def reroute(graph: dict[Ray, Ray], field, x0, y0) -> tuple[Ray, ...]:
    # Reroute graph with new vertex, and reroute back afterward
    state = {}
    new_vertices = []
    for dir in (U, D, L, R):
        x = x0 + XSTEP[dir]
        y = y0 + YSTEP[dir]
        inv_vertex = x, y, dir
        vertex = x, y, ROT[ROT[ROT[dir]]]

        if not (0 <= x < N and 0 <= y < M) or field[x, y]:
            # occupied or oob
            continue

        # look for vertices in reverse dir
        for parent in inv_raycast(inv_vertex, field, graph.keys()):
            state[parent] = graph[parent]
            graph[parent] = vertex

        # look for vertex in main dir
        graph[vertex] = raycast(vertex, field, graph.keys())
        new_vertices.append(vertex)
    yield new_vertices

    for parent, vertex in state.items():
        graph[parent] = vertex
    for vertex in new_vertices:
        del graph[vertex]


if __name__ == "__main__":
    # Parse input
    map = parse_np_matrix(dtype=str)

    [x_start], [y_start] = np.where(map == "^")
    N, M = map.shape
    map[x_start, y_start] = "."
    field: np.ndarray[bool] = map != "."

    vertices: set[Ray] = set()

    # Build graph
    for x0, y0 in product(range(N), range(M)):
        if field[x0, y0]:
            for dir in (U, D, L, R):
                x = x0 + XSTEP[dir]
                y = y0 + YSTEP[dir]
                if not (0 <= x < N and 0 <= y < M) or field[x, y]:
                    # occupied or oob
                    continue
                vertices.add((x, y, ROT[ROT[ROT[dir]]]))
    graph: dict[Ray, Ray] = {
        vertex: raycast(vertex, field, vertices) for vertex in vertices
    }
    del vertices  # use graph.keys() instead
    graph[OOB] = OOB

    # Traverse field
    x, y = int(x_start), int(y_start)
    dir = U
    cycles = 0
    lookups = 0
    visited = np.zeros_like(field, dtype=np.bool)

    for _ in tqdm(itertools.count(), disable=False):
        visited[x, y] = True

        # if boulder ahead, rotate
        while (x, y, ROT[dir]) in graph:
            dir = ROT[dir]

        # oob
        if not (0 <= x + XSTEP[dir] < N and 0 <= y + YSTEP[dir] < M):
            break

        # place boulder ahead
        xobs = x + XSTEP[dir]
        yobs = y + YSTEP[dir]

        # can't place boulders on the path we walked over already
        if not visited[xobs, yobs]:
            lookups += 1
            # considering alt path
            vx, vy, vdir = x, y, dir

            with reroute(graph, field, xobs, yobs) as new_vertices:
                # rotate on new boulder
                while (vx, vy, ROT[vdir]) in graph:
                    vdir = ROT[vdir]
                ray = vx, vy, vdir

                connection = raycast(ray, field, graph.keys())
                cycles += detect_cycle(graph, connection)

        x += XSTEP[dir]
        y += YSTEP[dir]
    print("Cycles", cycles)
    print("Reroutes", lookups)
    print("Visited", visited.sum())

# 2166 too high
# 1369 too low
# 1575 too low
# 1888 correct
