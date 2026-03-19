import sys

def limited_cycle(elements, n):
    for _ in range(n):
        for item in elements:
            yield item

def main():
    input_data = sys.stdin.read().splitlines()
    if len(input_data) < 2:
        return
    
    elements = input_data[0].split()
    try:
        n = int(input_data[1].strip())
    except (ValueError, IndexError):
        return

    result = limited_cycle(elements, n)
    sys.stdout.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()