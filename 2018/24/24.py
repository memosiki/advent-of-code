import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import count

from aoc_glue.input import parse_ints


class Side(Enum):
    imsys = auto()
    infection = auto()

    @staticmethod
    def get_opponent(self):
        return Side.imsys if self == Side.infection else Side.infection


@dataclass
class Group:
    units: int
    hp: int
    dmg: int
    initiative: int
    dmg_type: str = None
    weak: tuple[str] = field(default_factory=tuple)
    immune: tuple[str] = field(default_factory=tuple)
    side: Side = None
    targeted: bool = False
    uuid: int = field(default_factory=count().__next__)

    # uuid: int = field(default_factory=uuid4)

    @property
    def effective_power(self):
        return self.units * self.dmg

    def get_effective_damage(self, other: "Group"):
        return (
            1 + (self.dmg_type in other.weak) - (self.dmg_type in other.immune)
        ) * self.effective_power

    # def __str__(self):
    #     return f"{self.units=} {self.hp=} {self.immune=} {self.weak=} {self.dmg=} {self.dmg_type=} {self.initiative=}"


def get_immunities(line: str):
    if match := re.search(r"immune to ([\s\w,]+)[;)]", line):
        return tuple(re.findall(r"(\w+)", match[1]))
    return ()


def get_weaknesses(line: str):
    if match := re.search(r"weak to ([\s\w,]+)[;)]", line):
        return tuple(re.findall(r"(\w+)", match[1]))
    return ()


groups = []
with open("input", "r") as fd:
    fd.readline()

    def parse_group(line) -> Group:
        group = Group(*parse_ints(line))
        group.immune = get_immunities(line)
        group.weak = get_weaknesses(line)
        group.dmg_type = re.search(r" (\w+) damage", line)[1]
        return group

    while line := fd.readline().rstrip():
        group = parse_group(line)
        group.side = Side.imsys
        groups.append(group)
    fd.readline()
    for line in fd:
        group = parse_group(line)
        group.side = Side.infection
        groups.append(group)


def fight(groups: list[Group], boost: int) -> int:
    seen = set()
    # print(*groups, sep='\n\n')
    opponents: dict[Side, list[Group]] = {
        Side.imsys: [group for group in groups if group.side == Side.infection],
        Side.infection: [group for group in groups if group.side == Side.imsys],
    }
    for group in groups:
        if group.side == Side.imsys:
            group.dmg += boost
    while True:
        groups.sort(key=lambda x: (-x.effective_power, -x.initiative))
        targets: dict[int, Group | None] = {}
        for group in groups:
            max_dmg = -1
            target = None
            for opponent in opponents[group.side]:
                if opponent.targeted:
                    continue
                dmg = group.get_effective_damage(opponent)
                if dmg > max_dmg:
                    max_dmg = dmg
                    target = opponent
                elif max_dmg == dmg:
                    target = max(
                        opponent,
                        target,
                        key=lambda x: (x.effective_power, x.initiative),
                    )
            if target and max_dmg > 0:
                targets[group.uuid] = target
                target.targeted = True
        groups.sort(key=lambda x: -x.initiative)
        for group in groups:
            if group.units <= 0:
                continue
            target = targets.get(group.uuid)
            if target:
                target.units -= group.get_effective_damage(target) // target.hp
        for group in groups.copy():
            group.targeted = False
            if group.units <= 0:
                groups.remove(group)
                opponents[Side.get_opponent(group.side)].remove(group)
        state = tuple(group.units for group in groups)
        if state in seen:
            print("STALEMATE")
            return 0
        seen.add(state)
        if not all(opponents.values()):
            break
    winner = opponents[Side.imsys] or opponents[Side.infection]
    remaining_units = sum(group.units for group in winner)
    remaining_units *= (-1) ** (winner[0].side == Side.infection)
    return remaining_units


print("Surviving units without boost:", fight(deepcopy(groups), boost=0))
L = 0
R = 1_000_000
while L < R:
    m = (L + R) // 2
    print("Testing boost", m)
    if fight(deepcopy(groups), boost=m) > 0:
        R = m
    else:
        L = m + 1
optimal_boost = R
print(f"{optimal_boost=}, survivors:", fight(deepcopy(groups), boost=optimal_boost))
