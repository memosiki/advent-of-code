from typing import Self, Iterable


class _NodeIterator[T: "Node"]:
    __slots__ = "_node"

    def __init__(self, node: T):
        self._node = node

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self._node is None:
            raise StopIteration
        node = self._node
        self._node = self._node.next
        return node


class Node[T]:
    __doc__ = "Linked List"
    __slots__ = "next", "value"

    def __init__(self, value: T, next: Self = None):
        self.next = next
        self.value = value

    @classmethod
    def from_iter(cls, data: Iterable[T]) -> Self:
        head = prev = None
        for value in data:
            node = cls(value)
            if prev is None:
                head = node
            else:
                prev.next = node
            prev = node
        return head

    def __copy__(self) -> Self:
        return self.copy()

    def __iter__(self):
        return _NodeIterator(self)

    def copy(self) -> Self:
        node = self
        head = prev = Node(self.value)
        while node.next:
            prev.next = Node(node.next.value)
            node = node.next
        return head

    def __str__(self):
        return "".join(str(node.value) for node in self)

    def __repr__(self):
        return f"{super().__repr__()} -> {self.next!r}"
