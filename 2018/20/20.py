from collections import defaultdict
from dataclasses import dataclass
from queue import Queue

with open("input", "r") as fd:
    regex = fd.readline().rstrip()
regex = regex.strip("^$")
OPERATIONS = ("|", "+")


def tokenize(line):
    tokens = []
    token = ""

    def normalize_ops():
        # Skip empty branch in (any|)
        if len(tokens) > 1 and tokens[-2] == "|" and tokens[-1] == ")":
            tokens.pop()
            tokens.pop()
            tokens.append(")")
        # Add concatenation after any meaningful closing bracket
        if len(tokens) > 1 and tokens[-2] == ")" and tokens[-1] not in "+|)":
            displaced_token = tokens.pop()
            tokens.append("+")
            tokens.append(displaced_token)
        # opening bracket always equals to  + (
        if len(tokens) > 1 and tokens[-1] == "(" and tokens[-2] != "+":
            tokens.pop()
            tokens.append("+")
            tokens.append("(")

    for letter in line:
        if letter in "NEWS":
            token += letter
        else:
            if token:
                tokens.append(token)
                token = ""
                normalize_ops()
            tokens.append(letter)
            normalize_ops()
    if token:
        tokens.append(token)
        normalize_ops()
    return tokens


def reverse_polish_notation(tokens: list):
    stack = []
    expr = []
    for token in tokens:
        if token in OPERATIONS:
            if token == "|":
                # concatenation has higher priority
                while stack and stack[-1] == "+":
                    expr.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append("(")
        elif token == ")":
            while stack[-1] != "(":
                expr.append(stack.pop())
            stack.pop()
        else:
            expr.append(token)
    while stack:
        expr.append(stack.pop())
    return expr


@dataclass
class Node:
    token: str
    left: "Node" = None
    right: "Node" = None
    parent: "Node" = None

    @staticmethod
    def create_tree(tokens: list) -> "Node":
        """Create expression tree"""
        rpn = reverse_polish_notation(tokens)
        nodes = [Node(token) for token in rpn]
        stack = []
        for node in nodes:
            if node.token in OPERATIONS:
                right, left = stack.pop(), stack.pop()
                node.left = left
                node.right = right
                left.parent = right.parent = node
                stack.append(node)
            else:
                stack.append(node)
        assert len(stack) == 1, stack[1:]
        return stack[0]

    def __str__(self):
        return f"{self.token or '_'} ({self.left=} {self.right=})"

    def graph_repr(self, depth=0) -> str:
        """
        Pretty print as a vertical graph.
        """
        if not self:
            return ""
        return (
            "\t" * depth
            + (self.token or "_")
            + "\n"
            + Node.graph_repr(self.right, depth + 1)
            + Node.graph_repr(self.left, depth + 1)
        )

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    @staticmethod
    def move_along(dir, x, y):
        return {
            "E": (x + 1, y),
            "W": (x - 1, y),
            "N": (x, y - 1),
            "S": (x, y + 1),
        }[dir]


tokens = tokenize(regex)
# print(f"{regex=}")
print("With concatenations")
print(*tokens, sep="")
rpn = reverse_polish_notation(tokens)
# print(f"{rpn=}")
root = Node.create_tree(tokens)
print(root.graph_repr())

graph: dict[(int, int), set[(int, int)]] = defaultdict(set)


def dfs(node, starting_pos: tuple[*(int, int)]) -> tuple[*(int, int)]:
    """
    Dfs the node and return the final destinations reachable
    after traversing subtrees according to the operations.
    """
    match node.token:
        case "+":
            left_pos = dfs(node.left, starting_pos)
            right_pos = dfs(node.right, left_pos)
            return right_pos
        case "|":
            left_pos = dfs(node.left, starting_pos)
            right_pos = dfs(node.right, starting_pos)
            return (*left_pos, *right_pos)
        case _:
            assert node.is_leaf
            traversed_to = []
            assert starting_pos, node
            for x, y in starting_pos:
                for char in node.token:
                    xi, yi = Node.move_along(char, x, y)
                    graph[(x, y)].add((xi, yi))
                    graph[(xi, yi)]  # has side effect -- creates the node in graph
                    x, y = xi, yi
                traversed_to.append((x, y))
            return tuple(traversed_to)


dfs(root, ((0, 0),))


def pprint():
    """
    Pretty print whole visited field.
    Coords have to be scaled by 2 since the doors are between integers.
    """
    x = [point[0] for point in graph]
    y = [point[1] for point in graph]
    padding = 2
    max_x = max(x) * 2 + 1
    min_x = min(x) * 2
    max_y = max(y) * 2 + 1
    min_y = min(y) * 2
    N = max_x - min_x + 2 * padding
    offset_x = -min_x + padding
    M = max_y - min_y + 2 * padding
    offset_y = -min_y + padding

    pic = [["█"] * N for _ in range(M)]
    for (xs, ys), children in graph.items():
        for x1, y1 in children:
            (x0, x1) = sorted((xs * 2 + offset_x, x1 * 2 + offset_x))
            (y0, y1) = sorted((ys * 2 + offset_y, y1 * 2 + offset_y))
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    pic[y][x] = "."
            if x0 == x1:
                pic[y0 + 1][x0] = "-"
            if y0 == y1:
                pic[y0][x0 + 1] = "|"
    pic[0 + offset_y][0 + offset_x] = "X"
    for line in pic:
        print(*line, sep="")


pprint()
queue = Queue()
queue.put((0, 0))
visited: dict[(int, int), int] = {(0, 0): 0}
# BFS from (0,0) to look for max depth in graph
while not queue.empty():
    x, y = queue.get()
    depth = visited[(x, y)]
    for child in graph[(x, y)]:
        if child not in visited:
            visited[child] = depth + 1
            queue.put(child)

print("Max depth", max(visited.values()))
min_depth = 1_000
room_count = sum(depth >= min_depth for depth in visited.values())
print(f"Rooms at least {min_depth} deep:", room_count)
