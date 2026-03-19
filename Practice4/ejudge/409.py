import sys

def powers_of_two(n):
    for i in range(n + 1):
        yield str(1 << i)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    try:
        n = int(data[0])
        sys.stdout.write(" ".join(powers_of_two(n)) + "\n")
    except ValueError:
        pass

if __name__ == "__main__":
    main()