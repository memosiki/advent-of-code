import numpy as np
from tqdm import tqdm

patterns = [[]]

with open("input", "r") as f:
    for line in f:
        if line := line.rstrip():
            patterns[-1].append(list(line))
        else:
            patterns.append([])
answer = 0
for pattern in tqdm(patterns, ascii=True):
    padding = 1
    pattern = np.pad(np.array(pattern), padding, constant_values=".")
    print(pattern)
    bool_pattern = pattern == "#"
    # coord + 1 = count of rocks to the left on the axis
    counts = [
        np.apply_along_axis(sum, 1, bool_pattern).cumsum(),
        np.apply_along_axis(sum, 0, bool_pattern).cumsum(),
    ]
    found = False
    for axis in (1, 0):
        N = pattern.shape[axis]
        for y in range(1, N - 2):
            # [1, y] | [y+1, M-2]
            # reflection depth
            reflection_depth = min(y, N - 2 - y)
            # [y-rd, y] | [y+1, y + 1 + rd ]
            left_bound = y - reflection_depth + 1
            right_bound = y + 1 + reflection_depth - 1
            left_side_count = counts[axis][y] - counts[axis][left_bound - 1]
            right_side_count = counts[axis][right_bound] - counts[axis][y]
            if abs(right_side_count - left_side_count) == 1:
                coords = [..., ...]
                coords[axis] = range(y, left_bound - 1, -1)
                left_side = pattern[*coords]
                coords[axis] = range(y + 1, right_bound + 1)
                right_side = pattern[*coords]
                if (left_side != right_side).sum() == 1:
                    assert not found, pattern
                    print(f"mirrored at {y}")
                    if axis == 0:
                        answer += 100 * y
                    else:
                        answer += y
                    found = True
    assert found, pattern
print(answer)
