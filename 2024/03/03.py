import re
import sys

pattern = re.compile(r"mul\((-?\d+),(-?\d+)\)|(do)\(\)|(don't)\(\)")

if __name__ == "__main__":
    total = cond = 0
    enbld = True
    for line in sys.stdin:
        for a, b, do, dont in pattern.findall(line):
            if do:
                enbld = True
            if dont:
                enbld = False
            if do or dont:
                continue
            total += int(a) * int(b)
            cond += int(a) * int(b) * enbld

    print("Total", total)
    print("Conditional", cond)
