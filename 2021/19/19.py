import sys

from aoc_glue.input import parse_ints
import numpy as np
from numpy import pi
from scipy.spatial.distance import cdist
from tqdm import tqdm

from scipy.spatial.transform import Rotation as R

size_t = np.int_

NDIM = 3  # ONLY 3 dimensions supported

COVERAGE = 12  # there is probably a system to this
# COVERAGE = 5
# COVERAGE= 3

type Scanner = int
type Offset = np.ndarray[(NDIM,), size_t]
type Invert = bool
inverted = True

ROTATIONS = [
    # it has costed me an arm and a leg tinkering with scipy to get all these unique rotations
    R.from_euler("xyz", [-pi, -pi / 2, 0]),
    R.from_euler("xyz", [-pi, 0, -pi / 2]),
    R.from_euler("xyz", [-pi, pi / 2, 0]),
    R.from_euler("xyz", [-pi / 2, -pi / 2, 0]),
    R.from_euler("xyz", [-pi / 2, 0, -pi / 2]),
    R.from_euler("xyz", [-pi / 2, 0, -pi]),
    R.from_euler("xyz", [-pi / 2, 0, 0]),
    R.from_euler("xyz", [-pi / 2, 0, pi / 2]),
    R.from_euler("xyz", [-pi / 2, pi / 2, 0]),
    R.from_euler("xyz", [0, -pi / 2, 0]),
    R.from_euler("xyz", [0, 0, -pi / 2]),
    R.from_euler("xyz", [0, 0, pi]),
    R.from_euler("xyz", [0, pi / 2, 0]),
    R.from_euler("xyz", [0, 0, pi / 2]),
    R.from_euler("xyz", [0, 0, 0]),
    R.from_euler("xyz", [pi, 0, 0]),
    R.from_euler("xyz", [pi, 0, pi / 2]),
    R.from_euler("xyz", [pi, 0, pi]),
    R.from_euler("xyz", [pi / 2, -pi / 2, 0]),
    R.from_euler("xyz", [pi / 2, 0, -pi / 2]),
    R.from_euler("xyz", [pi / 2, 0, 0]),
    R.from_euler("xyz", [pi / 2, 0, pi / 2]),
    R.from_euler("xyz", [pi / 2, 0, pi]),
    R.from_euler("xyz", [pi / 2, pi / 2, 0]),
]

"""
All math is right handed, meaning:
       ^  +y
       |
       |
-x <---+--->  +x
       |
       |
       v  -y
"""

if __name__ == "__main__":
    beacon_map = {}
    idx = -1
    for line in sys.stdin:
        nums = parse_ints(line)
        if len(nums) == 1:
            idx += 1
        elif not nums:
            pass
        else:
            if idx not in beacon_map:
                beacon_map[idx] = np.array([nums])
            else:
                beacon_map[idx] = np.vstack(
                    (beacon_map[idx], np.array(nums)), dtype=size_t
                )

    Nscanners = len(beacon_map)
    origin = 0
    graph: list[list[tuple[Offset, R, Invert] | None]] = [
        [None] * Nscanners for _ in range(Nscanners)
    ]
    graph[origin][origin] = np.zeros(NDIM, dtype=size_t), R.identity(), False
    graph[origin][origin] = np.zeros(NDIM, dtype=size_t), R.identity(), True

    for scanner0 in tqdm(range(Nscanners)):
        beacons0 = beacon_map[scanner0]
        landmarks = {tuple(beacon) for beacon in beacons0}

        for scanner in range(scanner0 + 1, Nscanners):
            beacons = beacon_map[scanner]
            for rot in ROTATIONS:
                seen = set()
                for sbeacon in beacons:
                    # rotation and offset applied to beacons of scanner
                    #  maps them to beacons0 of scanner0
                    sbeacon0 = rot.apply(sbeacon).round()
                    for offset in beacons0 - sbeacon0:
                        offset: Offset
                        if tuple(offset) in seen:
                            continue
                        seen.add(tuple(offset))
                        translated = {
                            tuple(pos) for pos in rot.apply(beacons).round() + offset
                        }
                        if len(landmarks & translated) >= COVERAGE:
                            # translate scanner beacons to -> scanner0
                            graph[scanner0][scanner] = offset, rot, not inverted
                            # translate scanner0 beacons to -> scanner
                            graph[scanner][scanner0] = offset, rot, inverted

                            # print("Overlap", scanner0, scanner)
                            break
                    if graph[scanner0][scanner]:
                        break
                if graph[scanner0][scanner]:
                    break
        # break

    path: dict[int, list[tuple[Offset, R, Invert]]] = {origin: []}
    visited = {origin}

    def dfs(node, parent):
        offset, rot, inv = graph[parent][node]
        path[node] = path[parent].copy()
        path[node].append((offset, rot, inv))
        for child, translation in enumerate(graph[node]):
            if translation is not None and child not in visited:
                visited.add(child)
                dfs(child, node)

    dfs(origin, origin)
    """
    Translation as follows
    graph[a,b] : offset, rot
    dot_a = rot.apply(dot_b) + offset
    dot_b = rot.inv.apply(dot_a-offset)
    """

    true_scanners = np.empty((Nscanners, NDIM))
    # print true locations of scanners
    for scanner in range(Nscanners):
        position = np.array([0, 0, 0])
        for offset, rot, inv in reversed(path[scanner]):
            if inv == (not inverted):
                position = rot.apply(position) + offset
            else:
                position = rot.inv().apply(position - offset)
        true_scanners[scanner] = position
        print("Scanner", scanner, "at", position)

    # translate all beacons to scanner #0
    true_beacon_locations = set()
    for scanner in range(Nscanners):
        beacons = beacon_map[scanner]
        for offset, rot, inv in reversed(path[scanner]):
            if inv == (not inverted):
                beacons = rot.apply(beacons) + offset
            else:
                beacons = rot.inv().apply(beacons - offset)
        true_beacon_locations.update(tuple(beacon) for beacon in beacons.round())
    print("Unique beacons count", len(true_beacon_locations))

    # Part 2. Distance
    max_dist = (
        cdist(true_scanners, true_scanners, metric="cityblock").max().astype(size_t)
    )
    print("Max Manhattan distance", max_dist)
