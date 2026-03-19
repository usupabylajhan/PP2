import sys

def countdown(n):
    for i in range(n, -1, -1):
        yield str(i)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    try:
        n = int(input_data[0])
        for val in countdown(n):
            sys.stdout.write(val + "\n")
    except ValueError:
        pass

if __name__ == "__main__":
    main()