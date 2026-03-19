class student:
    def __init__(self,name,gpa):
        self.name = str(name)
        self.gpa = float(gpa)
    def nerd(self):
        return f"Name : {self.name} , GPA : {self.gpa}"
a = list(map(str , input().split()))
b = student(a[0],a[1])
print(b.nerd)