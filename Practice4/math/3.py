import math
x = int(input("Input number of sides: "))
y = int(input("Input the length of a side: "))
print("The area of the polygon is: ",end = '')
print(round((x * pow(y,2))/(4*math.tan(math.pi/x))))