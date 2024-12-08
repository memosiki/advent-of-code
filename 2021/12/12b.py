import sys
from collections import defaultdict


start = "start"
end = "end"
MAX_VISITS = 2


def main():
    graph: dict[str, list[str]] = defaultdict(list)
    for line in sys.stdin:
        a, b = line.rstrip().split("-")
        graph[b].append(a)
        graph[a].append(b)

    journeys = 0

    def dfs(
        node: str,
        visited: list[str],
        double_courtesy_used: bool,
    ):
        if node == end:
            print("->".join(visited))
            nonlocal journeys
            journeys += 1
            return
        for v in graph[node]:
            if v == start:
                continue
            if not (v.islower() and double_courtesy_used and v in visited):
                dfs(
                    v,
                    list((*visited, v)),
                    double_courtesy_used or v.islower() and v in visited,
                )

    dfs(start, list((start,)), False)
    print("Journeys count", journeys)


if __name__ == "__main__":
    main()
