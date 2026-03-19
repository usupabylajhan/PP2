import sys

def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    
    gen = even_generator(n)
    try:
        first = next(gen)
        sys.stdout.write(str(first))
        for val in gen:
            sys.stdout.write("," + str(val))
        sys.stdout.write("\n")
    except StopIteration:
        pass

if __name__ == "__main__":
    main()