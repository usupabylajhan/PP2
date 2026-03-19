import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    r = float(input_data[0])
    x1, y1 = float(input_data[1]), float(input_data[2])
    x2, y2 = float(input_data[3]), float(input_data[4])
    
    dist_ab = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    if r == 0:
        print(f"{dist_ab:.10f}")
        return

    d1_sq = x1*x1 + y1*y1
    d2_sq = x2*x2 + y2*y2
    d1 = math.sqrt(d1_sq)
    d2 = math.sqrt(d2_sq)
    
    dot_product = x1*x2 + y1*y2
    cos_gamma = max(-1.0, min(1.0, dot_product / (d1 * d2)))
    gamma = math.acos(cos_gamma)
    
    h = 0.0
    if dist_ab > 0:
        h = abs(x1 * y2 - y1 * x2) / dist_ab
    
    proj1 = (x2 - x1) * (-x1) + (y2 - y1) * (-y1)
    proj2 = (x1 - x2) * (-x2) + (y1 - y2) * (-y2)
    
    if h >= r or proj1 <= 0 or proj2 <= 0:
        print(f"{dist_ab:.10f}")
    else:
        alpha = math.acos(max(-1.0, min(1.0, r / d1)))
        beta = math.acos(max(-1.0, min(1.0, r / d2)))
        
        arc_angle = gamma - alpha - beta
        
        if arc_angle <= 0:
            print(f"{dist_ab:.10f}")
        else:
            len1 = math.sqrt(max(0, d1_sq - r*r))
            len2 = math.sqrt(max(0, d2_sq - r*r))
            arc_len = arc_angle * r
            print(f"{len1 + len2 + arc_len:.10f}")

if __name__ == "__main__":
    solve()