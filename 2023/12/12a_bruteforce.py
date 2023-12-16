import itertools
import re

from aoc_glue.input import parse_ints
from tqdm import tqdm

conditions = []
with open("input", "r") as f:
    for line in f:
        spans = parse_ints(line)
        field = bytearray(line.split()[0], encoding="utf-8")
        conditions.append((field, spans))

OPER = ord("#")
UNKN = ord("?")
NOSR = ord("_")
DOT = ord(".")
answer = 0
for field, spans in tqdm(conditions, ascii=True):
    pattern = re.compile(b"_*" + b"_+".join(b"#{%d}" % span for span in spans) + b"_*")
    present = sum(char == OPER for char in field)
    total = sum(spans)
    absent = [i for i in range(len(field)) if field[i] == UNKN]
    for i, char in enumerate(field):
        if char == UNKN:
            field[i] = NOSR
        if char == DOT:
            field[i] = NOSR
    for ids in itertools.combinations(absent, total - present):
        curr_field = field.copy()
        for id in ids:
            curr_field[id] = OPER
        # if pattern.match(b"".join(curr_field))
        if pattern.match(curr_field):
            # print(curr_field)
            answer += 1

print("Total arrangements", answer)
