from typing import Optional


def hash(line: bytes) -> int:
    hash = 0
    for char in line:
        hash = (hash + char) * 17 & 255
    return hash


class Node:
    next: "Node" = None
    prev: "Node" = None
    key: bytes
    data: int

    def __init__(self, key=b"", data=0):
        self.key = key
        self.data = data

    def find(self, key) -> Optional["Node"]:
        # O(N)
        curr = self
        while curr and curr.key != key:
            curr = curr.next
        return curr

    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev

    def insert(self, new: "Node"):
        # O(N)
        curr = self
        while curr.next:
            curr = curr.next
        new.prev = curr
        new.next = curr.next
        if curr.next:
            curr.next.prev = new
        curr.next = new

    def replace(self, key, data):
        self.key = key
        self.data = data


with open("input", "r") as fd:
    lenses = [(bytes(line, encoding="utf-8")) for line in fd.readline().rstrip().split(",")]

hashmap = [Node() for _ in range(256)]
for lens in lenses:
    if lens[-1:] == b"-":
        key = lens[:-1]
        node = hashmap[hash(key)].find(key)
        if node:
            node.remove()
    else:
        key, focus = lens.split(b"=")
        focus = int(focus)
        bucket = hashmap[hash(key)]
        node = bucket.find(key)
        if node:
            node.replace(key, focus)
        else:
            bucket.insert(Node(key, focus))

focusing_power = 0
for box_id, bucket in enumerate(hashmap, start=1):
    curr = bucket.next
    depth = 0
    while curr:
        depth += 1
        focusing_power += curr.data * depth * box_id
        # print(str(curr.key), focusing_power)
        curr = curr.next

print("Focusing power", focusing_power)
