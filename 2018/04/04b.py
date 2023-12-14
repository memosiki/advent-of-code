import re
import sys
from collections import defaultdict

MINUTES = 60
logs = sys.stdin.readlines()
logs.sort()
schedule = defaultdict(([0] * MINUTES).copy)

shift_start = re.compile(r".*Guard #(\d+) begins shift")
fall_asleep = re.compile(r".* 00:(\d{2})] falls asleep")
wake_up = re.compile(r".* 00:(\d{2})] wakes up")

for logline in logs:
    # no idea lmao
    match True:
        case True if re_match := shift_start.match(logline):
            (guard_id,) = re_match.groups()
            guard_id = int(guard_id)
        case True if re_match := fall_asleep.match(logline):
            (sleeps_from,) = re_match.groups()
            sleeps_from = int(sleeps_from)
        case True if re_match := wake_up.match(logline):
            (sleeps_to,) = re_match.groups()
            sleeps_to = int(sleeps_to)
            # all the mentioned vars have to be defined, otherwise panic
            for minute in range(sleeps_from, sleeps_to):
                schedule[guard_id][minute] += 1
        case _:
            assert False, logline


def pprint():
    for guard_id, hour in schedule.items():
        print(f"{guard_id:<5}", end="")
        for sleep_amount in hour:
            print(sleep_amount if sleep_amount else ".", end="")
        print()


# pprint()

max_sleepiness = 0
sleepiest_guard = -1
sleepiest_minute = -1
for guard_id, hour in schedule.items():
    for minute, sleep_amount in enumerate(hour):
        if sleep_amount > max_sleepiness:
            max_sleepiness = sleep_amount
            sleepiest_guard = guard_id
            sleepiest_minute = minute

print(sleepiest_minute, sleepiest_guard)
print(sleepiest_minute * sleepiest_guard)
