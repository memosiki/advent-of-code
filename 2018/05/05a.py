chain = []


def polar(a, b: str) -> bool:
    return a != b and a.lower() == b.lower()


def implode():
    while len(chain) >= 2 and polar(chain[-1], chain[-2]):
        chain.pop()
        chain.pop()


polymer = input()

for char in polymer:
    chain.append(char)
    implode()

for i in range(1, len(chain)):
    assert not polar(chain[i - 1], chain[i])

print(len(chain))
