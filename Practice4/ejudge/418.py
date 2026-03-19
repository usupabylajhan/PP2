import sys

def solve():
    input_data = sys.stdin.read().split()
    if len(input_data) < 4:
        return
    
    try:
        x1 = float(input_data[0])
        y1 = float(input_data[1])
        x2 = float(input_data[2])
        y2 = float(input_data[3])
        
        ay1 = abs(y1)
        ay2 = abs(y2)
        
        if ay1 + ay2 == 0:
            reflection_x = x1
        else:
            reflection_x = x1 + (x2 - x1) * (ay1 / (ay1 + ay2))
            
        reflection_y = 0.0
        
        print(f"{reflection_x:.10f} {reflection_y:.10f}")
        
    except (ValueError, ZeroDivisionError):
        pass

if __name__ == "__main__":
    solve()