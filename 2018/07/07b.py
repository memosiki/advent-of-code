import re
import sys
from collections import defaultdict

from sortedcontainers import SortedList, SortedSet

all_tasks = defaultdict(SortedSet)
inverse_graph = defaultdict(SortedSet)

pattern = re.compile(r"step (\w)", re.IGNORECASE)
for line in sys.stdin:
    [src, dest] = pattern.findall(line)
    all_tasks[src].add(dest)
    inverse_graph[dest].add(src)


def inverse_lexicographical(x: str) -> int:
    return -ord(x)


BASELINE_WORKLOAD = 60
WORKERS = 5


def workload(code: str) -> int:
    return BASELINE_WORKLOAD + ord(code) - ord("A") + 1


# find such vertices that no edges lead to them
available_tasks = [vertex for vertex in all_tasks if not inverse_graph[vertex]]
available_tasks = SortedList(available_tasks, key=inverse_lexicographical)
time = 0
done = 0
tasks: list = [None] * WORKERS
remainder = [-1] * WORKERS
# None is the placeholder for no task
while True:
    for i in range(WORKERS):
        # task ready
        if remainder[i] <= 0:
            for dest in all_tasks[tasks[i]]:
                inverse_graph[dest].remove(tasks[i])
                if not inverse_graph[dest]:
                    available_tasks.add(dest)
            tasks[i] = None
        if not tasks[i] and available_tasks:
            task = available_tasks.pop()
            tasks[i] = task
            remainder[i] = workload(task)
        remainder[i] -= 1
    print(time, *tasks, *remainder)
    if not any(tasks):
        break
    time += 1
time -= 1
print(time)
