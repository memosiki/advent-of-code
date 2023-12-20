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

low, high = 0, 1
total_low = total_high = 0
queue = Queue()
BUTTON_PRESSES = 1_000
total_low += BUTTON_PRESSES
for _ in tqdm(range(BUTTON_PRESSES)):
    queue.put(("roadcaster", low, None))
    while not queue.empty():
        name, pulse, sender = queue.get()
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
            total_high += output * len(modules[name])
            total_low += (1 - output) * len(modules[name])
            for child in modules[name]:
                queue.put((child, output, name))

print(f"{total_high=} {total_low=}")
print("Total mul: ", total_low * total_high)
