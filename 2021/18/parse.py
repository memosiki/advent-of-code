from typing import Iterable
from tree import Node, Pair, Leaf


def tokenize(text: str) -> Iterable[str]:
    idx = 0
    while idx < len(text):
        num = ""
        while text[idx].isdigit():
            num += text[idx]
            idx += 1
        if num:
            yield num
            continue
        yield text[idx]
        idx += 1


def build_tree(tokens: Iterable[str]) -> Node:
    fakeroot = Pair()
    stack: list[Pair[int]] = [fakeroot]
    for char in tokens:
        match char:
            case "[":
                parent = stack[-1]
                node = Pair(parent=parent)
                if parent.left is not None:
                    assert parent.right is None
                    parent.right = node
                else:
                    parent.left = node
                stack.append(node)
            case "]":
                stack.pop()
            case ",":
                pass
            case _ if char.isdigit():
                parent = stack[-1]
                leaf = Leaf(value=int(char), parent=parent)
                if parent.left is not None:
                    assert parent.right is None
                    parent.right = leaf
                else:
                    parent.left = leaf
            case _:
                assert False
    assert len(stack) == 1
    assert stack[0] is fakeroot
    assert fakeroot.right is None

    root = fakeroot.left
    root.parent = None
    return root
