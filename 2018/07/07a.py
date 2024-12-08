import re
import sys
from collections import defaultdict

from sortedcontainers import SortedList, SortedSet

graph = defaultdict(SortedSet)
inverse_graph = defaultdict(SortedSet)

pattern = re.compile(r"step (\w)", re.IGNORECASE)
for line in sys.stdin:
    [src, dest] = pattern.findall(line)
    graph[src].add(dest)
    inverse_graph[dest].add(src)


def inverse_lexicographical(x: str) -> int:
    return -ord(x)


def KahnTopologicalSort() -> list:
    linearization = []

    # find such vertices that no edges lead to them
    vertices = [vertex for vertex in graph if not inverse_graph[vertex]]

    # SortedList: insert O(logn), create O(n*logn)
    roots = SortedList(vertices, key=inverse_lexicographical)
    while roots:
        curr = roots.pop()
        linearization.append(curr)
        for dest in graph[curr]:
            inverse_graph[dest].remove(curr)
            if not inverse_graph[dest]:
                roots.add(dest)
    return linearization


linear = KahnTopologicalSort()
path = "".join(linear)
print(path)
