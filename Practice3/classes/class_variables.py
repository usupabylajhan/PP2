#1:
class Person:
    species = "Human"

p1 = Person()
p2 = Person()

print(p1.species)
print(p2.species)
#2:
class Person:
    species = "Human"

print(Person.species)
#3:
class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name

p1 = Person("Emil")
p2 = Person("Tobias")

print(p1.name, p1.species)
print(p2.name, p2.species)
#4:
class Person:
    species = "Human"
Person.species = "Homo sapiens"

p1 = Person()
print(p1.species)
#5:
class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        Person.count += 1

p1 = Person("Emil")
p2 = Person("Tobias")
p3 = Person("Linus")

print(Person.count)
