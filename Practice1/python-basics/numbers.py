import random
# Example 1
x = 1    # int
y = 2.8  # float
z = 1j   # complex

print(type(x))
print(type(y))
print(type(z))

# Example 2
x = 1
y = 999999999999999999999
z = -999999999999999999999

print(type(x),type(y),type(z))

# Example 3
x = 1.10
y = 1.0
z = -35.5e9

print(type(x),type(y),type(z))

# Example 4
x = 3+5j
y = 0+5j
z = 9-5j

print(x,y,z)
print(type(x),type(y),type(z))

# Example 5
print(random.randrange(10,100,10))