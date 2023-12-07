import sys
import string

ALPHABET = string.digits + "."

if __name__ == '__main__':
    answer = 0


    def process_line(prev: str, curr: str, next: str) -> int:
        parts_sum = 0

        def is_part_num(start, end: int) -> bool:
            for i in range(max(0, start - 1), min(end + 1, len(curr) - 1) + 1):
                if prev and prev[i] not in ALPHABET:
                    return True
                if next and next[i] not in ALPHABET:
                    return True
            return (start > 0 and curr[start - 1] not in ALPHABET) or (
                    end + 1 < len(curr) and curr[end + 1] not in ALPHABET)

        num, first_pos, digits = 0, 0, 0
        for i in range(len(curr)):
            if curr[i].isdigit():
                num = num * 10 + int(curr[i])
                if not digits:
                    first_pos = i
                digits += 1
            elif digits > 0:
                if is_part_num(first_pos, end=first_pos + digits - 1):
                    parts_sum += num
                num, first_pos, digits = 0, 0, 0
        else:
            if is_part_num(first_pos, end=first_pos + digits - 1):
                parts_sum += num
        return parts_sum


    prev, next = "", ""
    curr = input()
    for next in sys.stdin:
        next = next.rstrip()
        answer += process_line(prev, curr, next)
        prev, curr = curr, next
    next = ""
    answer += process_line(prev, curr, next)

    print(answer)
