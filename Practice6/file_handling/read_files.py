with open("data.txt") as f:
    print(f.read())

with open("data.txt") as f:
    for i, line in enumerate(f, 1):
        print(f"{i}: {line.rstrip()}")