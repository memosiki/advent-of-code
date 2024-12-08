import sys
from itertools import pairwise

from aoc_glue.input import parse_ints


def topological_sort(graph, inv_graph):
    orphans = []
    for v, parents in inv_graph.items():
        if not parents:
            orphans.append(v)
    order = dict.fromkeys(pages, 0)
    idx = 0
    while orphans:
        v = orphans.pop()
        order[v] = idx
        idx += 1
        for child in graph[v]:
            inv_graph[child].remove(v)
            if not inv_graph[child]:
                orphans.append(child)
    assert idx == N, "Not all nodes were visited"
    return order


if __name__ == "__main__":
    correct_metric = 0
    incorrect_metrix = 0

    edges = []
    for line in sys.stdin:
        nums = parse_ints(line)
        if not nums:
            break
        u, v = nums
        edges.append((u, v))

    for line in sys.stdin:
        pages = parse_ints(line)
        N = len(pages)

        graph = {v: set() for v in pages}
        inv_graph = {v: set() for v in pages}

        for u, v in edges:
            if u in pages and v in pages:
                graph[u].add(v)
                inv_graph[v].add(u)

        order = topological_sort(graph, inv_graph)

        ordering = [order[page] for page in pages]
        diffs = [b - a for a, b in pairwise(ordering)]
        ordered = all(diff > 0 for diff in diffs)
        if ordered:
            # Part 1.
            correct_metric += pages[N // 2]
        else:
            # Part 2.
            reorder = {idx: page for page, idx in order.items()}
            corrected_pages = [reorder[idx] for idx in range(N)]
            incorrect_metrix += corrected_pages[N // 2]
    print("Ordering metric of ordered pages", correct_metric)
    print("Ordering metric of disordered pages", incorrect_metrix)
