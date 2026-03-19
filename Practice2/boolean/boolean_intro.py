#1:
print(3 > 1)
print(3 == 1)
print(3 < 1)
#2:
x = 2
y = 3

if y > x:
  print("y is greater than x")
else:
  print("y is not greater than x")
#3:
print(bool(x))
print(bool(0))
#4:
def myFunction() :
  return y > x

if myFunction():
  print("YES!")
else:
  print("NO!")
#5:
print(isinstance(x,int))