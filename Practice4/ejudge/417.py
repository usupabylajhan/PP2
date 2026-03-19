import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    r = float(input_data[0])
    x1, y1 = float(input_data[1]), float(input_data[2])
    x2, y2 = float(input_data[3]), float(input_data[4])
    
    dx = x2 - x1
    dy = y2 - y1
    a = dx*dx + dy*dy
    b = 2 * (x1*dx + y1*dy)
    c = x1*x1 + y1*y1 - r*r
    
    if a == 0:
        if x1*x1 + y1*y1 <= r*r:
            print(f"{0.0:.10f}")
        else:
            print(f"{0.0:.10f}")
        return

    discriminant = b*b - 4*a*c
    
    if discriminant < 0:
        print(f"{0.0:.10f}")
        return
    
    sqrt_d = math.sqrt(discriminant)
    t1 = (-b - sqrt_d) / (2*a)
    t2 = (-b + sqrt_d) / (2*a)
    
    t_start = max(0.0, t1)
    t_end = min(1.0, t2)
    
    if t_start < t_end:
        segment_length = (t_end - t_start) * math.sqrt(a)
        print(f"{segment_length:.10f}")
    else:
        print(f"{0.0:.10f}")

if __name__ == "__main__":
    solve()