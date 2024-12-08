import string


def polar(a, b: str) -> bool:
    # can also use ord diff = ord A - ord a
    return a != b and a.lower() == b.lower()


def implode(chain):
    while len(chain) >= 2 and polar(chain[-1], chain[-2]):
        chain.pop()
        chain.pop()


polymer = input()

shortest_chain = len(polymer)
for excluded in zip(string.ascii_uppercase, string.ascii_lowercase):
    chain = []
    for char in polymer:
        if char not in excluded:
            chain.append(char)
            implode(chain)
    shortest_chain = min(shortest_chain, len(chain))

print(shortest_chain)
