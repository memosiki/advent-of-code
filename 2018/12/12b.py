from collections import defaultdict


def translate(line: str):
    return bytes(char == '#' for char in line)


def pprint(line: bytes | bytearray, offset=None):
    translation = {0: '.', 1: '#'}
    if offset: print(f"{offset:+>6} -->", end='')
    print(*map(translation.get, line), sep='')


rules = defaultdict(int)
with open("input", "r") as fd:
    pots = fd.readline().rstrip().split()[2]
    pots = bytes(translate(pots))
    fd.readline()
    for line in fd:
        [state, _, res] = line.split()
        rules[translate(state)] = int.from_bytes(translate(res))


def apply_rules_inplace(pots: bytes, new_pots: bytearray):
    for i in range(len(pots) - 5):
        new_pots[i + 2] = rules[pots[i:i + 5]]


def find_not():
    pass


seen: dict[bytes, (int, int)] = {}
empty = b'\x00'
plant = b'\x01'
time = 0
offset = 0  # offset from original left border position
while True:
    time += 1
    # add some padding
    new_pots = bytearray(empty * 5 + pots + empty * 5)
    pots = bytes(empty * 5 + pots + empty * 5)
    offset -= 5
    apply_rules_inplace(pots, new_pots)
    offset += new_pots.find(plant)
    pots = bytes(new_pots.strip(empty))
    if pots in seen:
        print("Found repeat", time)
        break
    seen[bytes(pots)] = (time, offset)

total_time = 50_000_000_000

# calculations for any cycle (. p.)\
#
# seen_by_time = {time: pots for pots, (time, _) in seen.items()}
# prev_time, prev_offset = seen[pots]
# cycle = time - prev_time
# total_time -= prev_time
# mirror_time = prev_time + total_time % cycle
#
# cycle_count = total_time // cycle
# offset_per_cycle = offset - prev_offset
# _, offset_within_cycle = seen[seen_by_time[mirror_time]]
# offset_within_cycle -= prev_offset
# offset = prev_offset + offset_per_cycle * cycle_count + offset_within_cycle
# print(f"{mirror_time} {offset=}")
# # 249999999860

seen_by_time = {time: pots for pots, (time, _) in seen.items()}
prev_time, prev_offset = seen[pots]
cycle = time - prev_time
assert cycle == 1
offset_per_cycle = offset - prev_offset
remaining_time = total_time - time
offset += offset_per_cycle * remaining_time

plant_num = 0
pprint(pots, offset)
print(f"{offset_per_cycle=}, {offset=}")
for i, char in enumerate(pots):
    if char == 1:
        plant_num += offset + i
print("Sum of all plant numbers", plant_num)
