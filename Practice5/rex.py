import re
#1:
n = input()
match = re.search(r'ab*', n)
if match: print(match.group())
else: print("No match")

#2:
match = re.search(r'ab{2,3}', n)
if match: print(match.group())
else: print("No match")

#3:
match = re.findall(r'\b[a-z]+(?:_[a-z]+)*\b', n)
if match:
    for m in match: print(m)  
else: print("No match")
   

#4:
match = re.findall(r'[A-Z][a-z]+', n)
if match:
    for m in match: print(m)
else: print("No match")
    

#5:
match = re.search(r'a.*b$', n)
if match: print(match.group())
else: print("No match")

#6:
s = re.sub(r',|\.|\s', r':', n)
print(s)

#7:
camel = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), n)
print(camel)

#8:
s = re.split(r"[A-Z]", n)
for i in s: print(i, end=" ")
print('\n')

#9:
spa = re.sub(r'(?<!^)(?=[A-Z])', ' ', n)
print(spa)

#10:
snake = re.sub(r'(?<!^)(?=[A-Z])', '_', n).lower()
print(snake)