import sys
from copy import deepcopy
from itertools import permutations
from typing import Callable
from tree import Node, Pair, Leaf
from parse import tokenize, build_tree

EXPLODE_DEPTH = 4
SPLIT_MASS = 10


def leftmost_pre_order_traversal(
    node: Node, depth: int, selector: Callable[[Node, int], bool]
) -> Node | None:
    assert node is not None

    if selector(node, depth):
        return node

    if node.is_leaf():
        return None

    lhs = leftmost_pre_order_traversal(node.left, depth + 1, selector)
    if lhs is not None:
        return lhs
    return leftmost_pre_order_traversal(node.right, depth + 1, selector)


def explosion_selector(node: Node, depth: int) -> bool:
    if node.is_leaf():
        return False
    if depth == EXPLODE_DEPTH:
        assert node.is_leaf_parent()
        return True
    return False


def split_selector(node: Node, _) -> bool:
    return node.is_leaf() and node.value >= SPLIT_MASS


def linearize_leafs(root: Node) -> list[Node]:
    leaves = []

    def dfs(node: Node):
        if node.is_leaf():
            leaves.append(node)
            return
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return leaves


def explode(node: Pair, root: Pair) -> None:
    leaves = linearize_leafs(root)
    if (idx := leaves.index(node.left) - 1) >= 0:
        leaves[idx].value += node.left.value
    if (idx := leaves.index(node.right) + 1) < len(leaves):
        leaves[idx].value += node.right.value

    if node.parent.left is node:
        node.parent.left = Leaf(value=0, parent=node.parent)
    else:
        node.parent.right = Leaf(value=0, parent=node.parent)


def split(node: Leaf) -> None:
    new_node = Pair(parent=node.parent)
    new_node.left = Leaf(value=node.value // 2, parent=new_node)
    new_node.right = Leaf(value=node.value // 2 + node.value % 2, parent=new_node)

    if node.parent.left is node:
        node.parent.left = new_node
    else:
        node.parent.right = new_node


def simplify(root: Node):
    # no operations allowed on the root
    while True:
        # print("State", root)
        node = leftmost_pre_order_traversal(root, 0, explosion_selector)
        if node is not None:
            # print("Exploding", node)
            explode(node, root)
            continue
        node = leftmost_pre_order_traversal(root, 0, split_selector)
        if node is not None:
            # print("Splitting", node)
            split(node)
            continue
        break


def add(lhs: Node, rhs: Node) -> Node:
    new_root = Pair(parent=None)
    new_root.left = lhs
    lhs.parent = new_root
    new_root.right = rhs
    rhs.parent = new_root
    return new_root


def magnitude(node: Node) -> int:
    if node.is_leaf():
        return node.value
    return magnitude(node.left) * 3 + magnitude(node.right) * 2


if __name__ == "__main__":
    # input
    nums = [build_tree(tokenize(line.rstrip())) for line in sys.stdin]

    # Part 1. All additions
    lhs = deepcopy(nums[0])
    for rhs in nums[1:]:
        lhs = add(lhs, deepcopy(rhs))
        simplify(lhs)
    print("Addition result", lhs)
    print("Magnitude", magnitude(lhs))

    # Part 2. Largest pair
    max_magnitude = 0
    largest_pair = None
    for lhs, rhs in permutations(nums, 2):
        res = add(deepcopy(lhs), deepcopy(rhs))
        simplify(res)
        if max_magnitude < (m := magnitude(res)):
            max_magnitude = m
            largest_pair = lhs, rhs
    print("Largest pair", *largest_pair)
    print("Max magnitude", max_magnitude)
