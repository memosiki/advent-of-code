from dataclasses import dataclass, field

regex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
#
# with open("input", "r") as fd:
#     regex = fd.readline().rstrip()
regex = regex.strip("^$")
OPERATIONS = ("|", "+")


def tokenize(line):
    tokens = []
    token = ""

    def check_skipped_ops():
        # Add empty token to branch or empty
        if len(tokens) > 1 and tokens[-2] == "|" and tokens[-1] == ")":
            tokens.pop()
            tokens.append("")
            tokens.append(")")
        # Add concatenation after meaningful closing bracket
        if (
            len(tokens) > 1
            and tokens[-2] == ")"
            and tokens[-1] not in OPERATIONS + (")",)
        ):
            displaced_token = tokens.pop()
            tokens.append("+")
            tokens.append(displaced_token)
        if len(tokens) > 1 and tokens[-1] == "(":  # token[-2] is reuqired to exist
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
                check_skipped_ops()
            tokens.append(letter)
            check_skipped_ops()
    if token:
        tokens.append(token)
        check_skipped_ops()
    return tokens


def reverse_polish_notation(tokens: list):
    stack = []
    expr = []
    for token in tokens:
        if token in OPERATIONS:
            # if token == "|":
            #     while stack and stack[-1] == "+":
            #         expr.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append("(")
        elif token == ")":
            while stack[-1] != "(":
                expr.append(stack.pop())
            stack.pop()
        else:  # text
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
    right_brother: "Node" = None
    left_brother: "Node" = None
    depths: dict[tuple, int] = field(default_factory=dict)

    @staticmethod
    def create_tree(tokens: list) -> "Node":
        """Create expression tree"""
        rpn = reverse_polish_notation(tokens)
        nodes = [Node(token) for token in rpn]
        stack = []
        for node in nodes:
            if node.token in OPERATIONS:
                right, left = stack.pop(), stack.pop()
                left.right_brother = right
                right.left_brother = left
                node.left = left
                node.right = right
                left.parent = right.parent = node
                stack.append(node)
            else:
                stack.append(node)
        assert len(stack) == 1, stack[1:]
        return stack[0]

    def __str__(self):
        return f"{self.token} ({self.left=} {self.right=})"

    def to_graph(self, depth=0) -> str:
        if not self:
            return ""
        return (
            "\t" * depth
            + (self.token or '""')
            + "\n"
            + Node.to_graph(self.left, depth + 1)
            + Node.to_graph(self.right, depth + 1)
        )


def move(x, y, dir):
    return {
        "E": (x + 1, y),
        "W": (x - 1, y),
        "N": (x, y - 1),
        "S": (x, y + 1),
    }[dir]


tokens = tokenize(regex)
print(f"{regex=}")
print(f"{tokens=}")
rpn = reverse_polish_notation(tokens)
print(rpn)
root = Node.create_tree(tokens)
print(root.to_graph())

# DFS
stack = []
seen: dict[tuple, int] = {}
stack.append(root)
# x = y = 0
root.parent = Node("")  # fake node
root.parent.depths[(0, 0)] = 0

# ЛКП
while stack:
    node: Node = stack.pop()
    if node.left_brother:
        assert len(node.depths) <= 1, node.token
        node.depths = node.left_brother.depths.copy()
    else:
        node.depths = node.parent.depths.copy()
    match node.token:
        case "+":
            stack.append(node.right)
            stack.append(node.left)
            node.left.depths = node.depths.copy()
            # node.right will look at left brother depths
        case "|":
            stack.append(node.right)
            stack.append(node.left)
            node.right.depths = node.depths.copy()
            node.left.depths = node.depths.copy()
        case _:
            assert node.left is None and node.right is None
            for (x, y), depth in node.depths.items():
                for char in node.token:
                    depth += 1
                    x, y = move(x, y, char)
                    seen[(x, y)] = min(seen.get((x, y), float("inf")), depth)
                # node.parent.depths[(x, y)] = min(seen.get((x, y), float("inf")), depth)
print(seen)
print("Deepest", max(seen.values()))
