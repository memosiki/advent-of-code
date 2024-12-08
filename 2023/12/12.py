import functools

from aoc_glue.input import parse_ints

field = []
with open("input", "r") as f:
    for line in f:
        spans = tuple(parse_ints(line))
        pattern = line.split()[0]
        field.append((pattern, spans))


@functools.cache
def apply(line: str, spans: tuple[int]) -> int:
    if not spans:
        return line.count("#") == 0
    if not line or spans[0] > len(line):
        return 0
    arrangements = 0
    if line[0] != "#":
        arrangements += apply(line[1:], spans)
    span = spans[0]
    if line.count(".", 0, span) == 0 and (span == len(line) or line[span] != "#"):
        arrangements += apply(line[span + 1 :], spans[1:])
    return arrangements


def unfold(pattern: str) -> str:
    return "?".join((pattern,) * 5)


arrangements = 0
for pattern, spans in field:
    arrangements += apply(pattern, spans)
print("Arrangements", arrangements)

arrangements = 0
for pattern, spans in field:
    arrangements += apply(unfold(pattern), spans * 5)
print("Unfolded arrangements", arrangements)
