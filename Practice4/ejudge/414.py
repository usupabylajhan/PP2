import sys
from datetime import datetime, timezone, timedelta

def parse_iso_with_tz(line):
    # Format: YYYY-MM-DD UTC+HH:MM or YYYY-MM-DD UTC-HH:MM
    parts = line.strip().split()
    date_str = parts[0]
    tz_str = parts[1].replace("UTC", "")
    
    # Parse date to midnight
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Parse timezone offset
    sign = 1 if tz_str[0] == '+' else -1
    hours = int(tz_str[1:3])
    minutes = int(tz_str[4:6])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    
    # Create aware datetime
    return dt.replace(tzinfo=timezone(offset))

def main():
    lines = sys.stdin.read().splitlines()
    if len(lines) < 2:
        return
    
    try:
        dt1 = parse_iso_with_tz(lines[0])
        dt2 = parse_iso_with_tz(lines[1])
        
        # Calculate absolute difference in seconds
        diff_seconds = abs((dt1 - dt2).total_seconds())
        
        # Convert to full days (floor of total seconds / 86400)
        days = int(diff_seconds // 86400)
        sys.stdout.write(str(days) + "\n")
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()