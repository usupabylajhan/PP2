import sys
from datetime import datetime, timezone, timedelta

def parse_dt(line):
    parts = line.strip().split()
    date_part = parts[0]
    time_part = parts[1]
    tz_part = parts[2].replace("UTC", "")
    
    dt_str = f"{date_part} {time_part}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    
    sign = 1 if tz_part[0] == '+' else -1
    h = int(tz_part[1:3])
    m = int(tz_part[4:6])
    tz = timezone(timedelta(hours=h, minutes=m) * sign)
    
    return dt.replace(tzinfo=tz)

def main():
    input_data = sys.stdin.read().strip().split('\n')
    if len(input_data) < 2:
        return
    
    try:
        start_dt = parse_dt(input_data[0])
        end_dt = parse_dt(input_data[1])
        
        duration = int((end_dt - start_dt).total_seconds())
        sys.stdout.write(str(duration) + "\n")
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()