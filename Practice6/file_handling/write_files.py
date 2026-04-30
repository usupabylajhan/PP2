lines = ["Alice, 30", "Bob, 25", "Carol, 35"]

with open("data.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

with open("data.txt", "a") as f:
    f.write("David, 28\n")

with open("data.txt") as f:
    print(f.read())