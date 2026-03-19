#!/usr/bin/env python3
import sys
from datetime import datetime, timezone, timedelta

def parse(line):
    line = line.strip()
    date_part, tz_part = line.split()
    y, m, d = map(int, date_part.split('-'))
    # tz_part like 'UTC+05:30' or 'UTC-00:00'
    sign = 1 if tz_part[3] == '+' else -1
    th = int(tz_part[4:6])
    tm = int(tz_part[7:9])
    off = timedelta(hours=th, minutes=tm) * sign
    tz = timezone(off)
    dt = datetime(y, m, d, 0, 0, 0, tzinfo=tz)
    return (y, m, d, tz, dt)

def is_leap(y):
    return (y%4==0 and y%100!=0) or (y%400==0)

birth_line = sys.stdin.readline()
cur_line = sys.stdin.readline()
by, bm, bd, birth_tz, birth_dt = parse(birth_line)
_, _, _, cur_tz, cur_dt = parse(cur_line)

cur_ts = int(cur_dt.timestamp())

start_year = cur_dt.year
# iterate a few years forward (birthday occurs every year after Feb29->Feb28 rule)
for y in range(start_year, start_year + 3):
    day = bd
    if bm == 2 and bd == 29 and not is_leap(y):
        day = 28
    # construct candidate in birth timezone local midnight
    try:
        cand = datetime(y, bm, day, 0, 0, 0, tzinfo=birth_tz)
    except ValueError:
        # shouldn't happen, but skip invalid dates
        continue
    cand_ts = int(cand.timestamp())
    if cand_ts >= cur_ts:
        diff = cand_ts - cur_ts
        if diff == 0:
            print(0)
        else:
            days = (diff + 86400 - 1) // 86400
            print(days)
        sys.exit(0)

# fallback (shouldn't be reached)
# compute next year's birthday
y = start_year + 3
day = bd
if bm == 2 and bd == 29 and not is_leap(y):
    day = 28
cand = datetime(y, bm, day, 0, 0, 0, tzinfo=birth_tz)
diff = int(cand.timestamp()) - cur_ts
print(0 if diff == 0 else (diff + 86400 - 1) // 86400)