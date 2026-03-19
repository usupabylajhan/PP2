import sys

def fibonacci_generator(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    try:
        n = int(data[0])
    except ValueError:
        return

    if n <= 0:
        return

    gen = fibonacci_generator(n)
    try:
        sys.stdout.write(str(next(gen)))
        for val in gen:
            sys.stdout.write("," + str(val))
        sys.stdout.write("\n")
    except StopIteration:
        pass

if __name__ == "__main__":
    main()