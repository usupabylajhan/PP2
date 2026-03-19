# Example 1
x = 1
y = "hello"
print(type(x),type(y))

# Example 2
x = str(3)
y = int(3)
z = float(3)
print(x,y,z)

# Example 3
_ = 1#'-' - illegal
A = 1#A A - illelag
A2 = 1 #2A - illegal

# Example 4
x,y,z = 1,2,3
print(x,y,z)
x = y = z = "a"
print(x+y+z)
numbers = [1,2,3]
x, y, z = numbers
print(x,y,z)

# Example 5
x = "1"

def myfunc():
  global x
  x = "2"

myfunc()

print(x)