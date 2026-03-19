import sys

def divisibility_generator(n):
    for i in range(0, n + 1, 12):
        yield i

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    try:
        n = int(data[0])
    except ValueError:
        return
    
    gen = divisibility_generator(n)
    try:
        first = next(gen)
        sys.stdout.write(str(first))
        for val in gen:
            sys.stdout.write(" " + str(val))
        sys.stdout.write("\n")
    except StopIteration:
        pass

if __name__ == "__main__":
    main()