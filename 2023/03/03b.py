import sys
from collections import defaultdict
from pprint import pprint

GEAR = "*"

if __name__ == "__main__":
    gears = defaultdict(list)

    def process_line(line_id: int, prev: str, curr: str, next: str) -> int:
        parts_sum = 0

        def attach_gears(vertical_pos, num, start, end: int) -> None:
            for i in range(max(0, start - 1), min(end + 1, len(curr) - 1) + 1):
                if prev and prev[i] == GEAR:
                    gears[(vertical_pos - 1, i)].append(num)
                if next and next[i] == GEAR:
                    gears[(vertical_pos + 1, i)].append(num)
            if start > 0 and curr[start - 1] == GEAR:
                gears[(vertical_pos, start - 1)].append(num)
            if end + 1 < len(curr) and curr[end + 1] == GEAR:
                gears[(vertical_pos, end + 1)].append(num)

        num, first_pos, digits = 0, 0, 0
        for i in range(len(curr)):
            if curr[i].isdigit():
                num = num * 10 + int(curr[i])
                if not digits:
                    first_pos = i
                digits += 1
            elif digits > 0:
                attach_gears(line_id, num, first_pos, end=first_pos + digits - 1)
                num, first_pos, digits = 0, 0, 0
        else:
            attach_gears(line_id, num, first_pos, end=first_pos + digits - 1)
        return parts_sum

    prev, next = "", ""
    curr = input()
    line_id = 0
    for next in sys.stdin:
        next = next.rstrip()
        process_line(line_id, prev, curr, next)
        prev, curr = curr, next
        line_id += 1
    next = ""
    process_line(line_id, prev, curr, next)

    pprint(gears)
    answer = sum(
        details[0] * details[1] for details in gears.values() if len(details) == 2
    )
    print(answer)
