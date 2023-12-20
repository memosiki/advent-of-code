import operator
from functools import reduce
from queue import Queue

from tqdm import tqdm

modules: dict[str, tuple] = {}
types: dict[str, str] = {}
off: dict[str, bool] = {}
conj: dict[str, dict[str, bool]] = {}

with open("input", "r") as f:
    for line in f:
        name, dsts = line.rstrip().split(" -> ")
        type, name = name[0], name[1:]
        modules[name] = tuple(dsts.split(", "))
        types[name] = type


def get_inputs(conj):
    inputs = {}
    for name, dsts in modules.items():
        if conj in dsts:
            inputs[name] = False
    return inputs


for name, connected in modules.copy().items():
    off[name] = False
    conj[name] = get_inputs(name)
    for child in connected:
        types.setdefault(child, "")

pbar = tqdm()
low, high = 0, 1
queue = Queue()
button_presses = 0
reached = False


def print_all_inputs():
    print("All inputs")
    for module, inputs in conj.items():
        print(types[module], module, "<--", *inputs.keys())


# print_all_inputs()
"""
rx <- dd

& dd <-- nx sp cc jq

& nx <-- ft
& sp <-- qr
& cc <-- lk
& jq <-- lz

& ft <-- jn hq sz fr qc pl qh
& qr <-- mj rv vl jj cz dq bz mb zj
& lk <-- gm qm vg db mh sb ks
& lz <-- mv ts xc nk vb hd xl dv
"""
rx_inputs = ("nx", "sp", "cc", "jq")

prev = {name: 0 for name in rx_inputs}
rx_cycles = {name: set() for name in rx_inputs}
MAX_PRESSES = 10_000
for _ in range(MAX_PRESSES):
    queue.put(("roadcaster", low, None))
    button_presses += 1
    pbar.update(1)
    while not queue.empty():
        name, pulse, sender = queue.get()

        if pulse == low and name in rx_inputs:
            # writing down low cycles for rx inputs
            cycle = button_presses - prev[name]
            rx_cycles[name].add(cycle)
            prev[name] = button_presses

        output = None
        if types[name] == "b":
            output = pulse
        elif types[name] == "%":
            if pulse == low:
                off[name] ^= 1
                output = off[name]
        elif types[name] == "&":
            conj[name][sender] = pulse
            output = not all(conj[name].values())
        if output is not None:
            for child in modules[name]:
                queue.put((child, output, name))

print("Rx inputs cycles", rx_cycles)
assert all(map(lambda x: len(x) == 1, rx_cycles.values()))
cycles = [cycle.pop() for cycle in rx_cycles.values()]
# print("Overall cycle", reduce(math.lcm, cycles, 1))
print("Overall cycle", reduce(operator.mul, cycles, 1))
