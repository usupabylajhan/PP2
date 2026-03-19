import sys

def square_generator(n):
    for i in range(1, n + 1):
        yield i * i

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    for square in square_generator(n):
        print(square)

if __name__ == "__main__":
    main()