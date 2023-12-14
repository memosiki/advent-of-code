import sys

# also includes newlines, doesn't affect the task in any way
ids = sys.stdin.readlines()
n = len(ids)


def diff2(a: str, b: str) -> bool:
    cnt = 0
    # returns if strings differ by at least 2 symbols
    for chara, charb in zip(a, b):
        if chara != charb:
            cnt += 1
        if cnt > 1:
            return False
    # by definition there are only unique strings
    assert cnt == 1
    return True


for k, idl in enumerate(ids):
    for idr in ids[k + 1 :]:
        if diff2(idl, idr):
            intersection = "".join(a for a, b in zip(idr, idl) if a == b)
            print(intersection)
            exit(0)  # goto: kys
