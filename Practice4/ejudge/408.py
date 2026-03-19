import sys

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def prime_generator(n):
    for i in range(2, n + 1):
        if is_prime(i):
            yield str(i)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    try:
        n = int(data[0])
    except ValueError:
        return

    primes = prime_generator(n)
    sys.stdout.write(" ".join(primes) + "\n")

if __name__ == "__main__":
    main()