import dataclasses


@dataclasses.dataclass(eq=False)
class Leaf[T]:
    value: T
    parent: "Pair[T]"

    def __str__(self):
        return str(self.value)

    @staticmethod
    def is_leaf():
        return True


@dataclasses.dataclass(eq=False)
class Pair[T]:
    parent: "Pair[T] | None" = None
    left: "Pair[T] | Leaf[T]" = None
    right: "Pair[T] | Leaf[T]" = None

    def __str__(self):
        return f"[{self.left},{self.right}]"

    @staticmethod
    def is_leaf():
        return False

    def is_leaf_parent(self):
        return self.right.is_leaf() and self.left.is_leaf()


type Node[T] = Pair[T] | Leaf[T]
