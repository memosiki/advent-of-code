import re
from typing import List


def golang_format(container: List):
    return str(container).translate(str.maketrans("[]", "{}"))


COUNT = 3
columns = [[] for _ in range(COUNT)]
with open("input", "r") as f:
    for row in f.readlines():
        if not re.match(r"\s*\[", row):
            break
        for i in range(COUNT):
            loc = i * 3 + i + 1
            if loc < len(row) and (crate := row[loc]) != " ":
                columns[i].insert(0, crate)
        print(golang_format(columns))
