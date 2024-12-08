import operator
import re
from collections import defaultdict
from functools import reduce

from ranges import Range, RangeSet
from frozendict import frozendict

Details = frozendict[str, RangeSet]
boundary = Range("[1,4000]")
ruleset = defaultdict(list)
terminal = {"A": "A", "R": "R"}
with open("input", "r") as fd:
    while line := fd.readline().rstrip().rstrip("}"):
        workflow, *rules, terminal[workflow] = re.split(r"[,{]", line)
        for rule in rules:
            letter, op, *_ = list(rule)
            cond, state = rule[2:].split(":")
            if op == ">":
                range = Range(start=int(cond), include_start=False) & boundary
            else:
                range = Range(end=int(cond), include_end=False) & boundary
            ruleset[workflow].append((range, letter, state))
    pass  # skip the rest of the input


def span(r: Range) -> int:
    """Count integers in Range"""
    return r.end - r.start + 1 - (not r.include_end) - (not r.include_start)


def combinations(vars: Details) -> int:
    counts = [sum(span(r) for r in rangeset.ranges()) for letter, rangeset in vars.items()]
    assert any(counts)
    return reduce(operator.mul, counts, 1)


# dfs expression tree
def dfs(name: str, rating: Details):
    if name == "R":
        return
    if name == "A":
        global total_accepted
        total_accepted += combinations(rating)
        return
    for cond, letter, state in ruleset[name]:
        narrowed_scope: RangeSet = cond & rating[letter]
        if narrowed_scope:  # if Range is non-empty
            dfs(state, rating.set(letter, narrowed_scope))
        # Apply the opposite condition and proceed to the next rule
        rating = rating.set(letter, rating[letter] & cond.complement())
    # lurk into the terminal (aka otherwise) condition
    dfs(terminal[name], rating)


total_accepted = 0
rating = frozendict({i: RangeSet(boundary) for i in "xmas"})
dfs("in", rating)
print(f"{total_accepted=}")
