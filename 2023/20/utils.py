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

trans = {"roadcaster": 0}
modules1 = modules.copy()
del modules1["roadcaster"]
trans = trans | {name: i for i, name in enumerate(modules1, start=1)}
rev = {i: name for (name, i) in trans.items()}


def translate(names):
    return map(str, map(trans.get, names))


def transtype(type):
    return {"b": "0", "%": "1", "&": "2"}[type]


def to_array(elems):
    return "{" + ",".join(str(elem) for elem in elems) + "}"


def to_map(elems):
    return "{" + ",".join(f"{elem}:false" for elem in elems) + "}"


N = len(modules)
connections = []
typesi = []
conjsi = []
for i in range(N):
    name = rev[i]
    children = modules[name]
    connections.append(to_array(translate(children)))
    typesi.append(transtype(types[name]))
    conjsi.append(to_map(translate(conj[name].keys())))
print(f"{N=}")
# print(f"{trans["rx"]=}")
print("[][]int", to_array(connections), sep="")
print("[]int", to_array(typesi), sep="")
print("[]map[int]bool", to_array(conjsi), sep="")
print(len(conjsi))
