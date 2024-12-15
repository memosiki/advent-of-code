import sys

import ffmpeg
import numpy as np
from aoc_glue.input import parse_ints
from PIL import Image as im

# N = 11
N = 101
# M = 7
M = 103
STEPS = 8006
if __name__ == "__main__":
    robots = []
    for line in sys.stdin:
        x, y, vx, vy = parse_ints(line)
        robots.append((x, y, vx, vy))
    for step in range(STEPS):
        for i, (x, y, vx, vy) in enumerate(robots):
            robots[i] = (x + vx) % N, (y + vy) % M, vx, vy
        if 7800 <= step <= STEPS:
            canvas = np.zeros((N, M), dtype=np.bool_)
            for x, y, _, _ in robots:
                canvas[x, y] = True
            im.fromarray(canvas).save(f"frames/frame{step:05d}.png")
        # print("Step", step + 1)
        # pprint_spelled(canvas, t=True)
(
    ffmpeg.input("frames/frame*.png", pattern_type="glob", framerate=10)
    .output("movie.mp4")
    .run(overwrite_output=True)
)
