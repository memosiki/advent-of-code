import sys
from collections import defaultdict

start = "start"
end = "end"


def main():
    graph = defaultdict(list)
    for line in sys.stdin:
        a, b = line.rstrip().split("-")
        graph[b].append(a)
        graph[a].append(b)

    journeys = 0

    def dfs(node: str, visited: list[str] | frozenset[str]):
        if node == end:
            print("->".join(visited))
            nonlocal journeys
            journeys += 1
            return
        for v in graph[node]:
            if not (v.islower() and v in visited):
                dfs(v, list((*visited, v)))

    dfs(start, [start])
    print("Journeys count", journeys)


if __name__ == "__main__":
    main()
