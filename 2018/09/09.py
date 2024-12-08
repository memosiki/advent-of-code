from tqdm import tqdm


class Node:
    next: "Node"
    prev: "Node"
    data: int

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __str__(self) -> str:
        nums = [self.data]
        curr = self.next
        while curr != self:
            nums.append(curr.data)
            curr = curr.next
        return "->".join(f"{data:<3}" for data in nums)

    def offset(self, count=1) -> "Node":
        curr = self
        getter = "next" if count >= 0 else "prev"
        for i in range(abs(count)):
            curr = getattr(curr, getter)
        return curr

    def insert(self, payload) -> "Node":
        new = Node(payload, self, self.next)
        self.next.prev = new
        self.next = new
        return new

    def remove(self) -> int:
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.data


players = 466
marbles = 7143600

scores = [0] * players
special = set(23 * i for i in range(marbles // 23 + 10))

curr = Node(data=0)
curr.prev = curr.next = curr
for marble in tqdm(range(1, marbles)):
    if marble in special:
        rmd = curr.offset(-7)
        curr = rmd.offset(1)
        scores[marble % players] += rmd.remove() + marble
    else:
        curr = curr.offset(1).insert(marble)
print(max(scores))
