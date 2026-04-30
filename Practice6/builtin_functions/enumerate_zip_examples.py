fruits = ["apple", "banana", "cherry"]
names  = ["Alice", "Bob", "Carol"]
scores = [92, 78, 88]

for i, fruit in enumerate(fruits, 1):
    print(i, fruit)

for name, score in zip(names, scores):
    print(name, score)

print(type(42), isinstance(42, int))
print(int("10"), float("3.14"), str(99), list("abc"))