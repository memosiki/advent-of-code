import operator
import re
from collections import defaultdict

from aoc_glue.input import parse_ints

ruleset = defaultdict(list)
ruleset.update(**{"A": (lambda _: "A",), "R": (lambda _: "R",)})
terminal = {}
details = []


def get_rule(op, letter, cond, state):
    return lambda x: state if op(x[letter], int(cond)) else None


with open("input", "r") as fd:
    while line := fd.readline().rstrip().rstrip("}"):
        workflow, *rules, terminal[workflow] = re.split(r"[,{]", line)
        for rule in rules:
            letter, op, *_ = list(rule)
            cond, state = rule[2:].split(":")
            op = operator.gt if op == ">" else operator.lt
            ruleset[workflow].append(get_rule(op, letter, cond, state))
    for line in fd:
        details.append(dict(zip("xmas", parse_ints(line))))

total_rating = 0
for detail in details:
    # starting workflow
    workflow = "in"
    accounted_for = False
    while not accounted_for:
        for rule in ruleset[workflow]:
            match res := rule(detail):
                case None:
                    pass
                case "A":
                    total_rating += sum(detail.values())
                    accounted_for = True
                case "R":
                    accounted_for = True
                case _:
                    workflow = res
            if res:
                break
        else:
            workflow = terminal[workflow]
print(f"{total_rating=}")
