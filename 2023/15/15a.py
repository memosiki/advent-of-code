def hash(line: bytes) -> int:
    hash = 0
    for char in line:
        hash += char
        hash = hash * 17 & 255
    return hash


with open("input", "r") as fd:
    answer = sum(hash(bytes(line, encoding="utf-8")) for line in fd.readline().rstrip().split(","))

print(answer)
