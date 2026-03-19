import sys

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    
    a = int(data[0])
    b = int(data[1])
    
    for val in squares(a, b):
        sys.stdout.write(str(val) + "\n")

if __name__ == "__main__":
    main()