import os
import shutil

os.makedirs("inbox", exist_ok=True)
os.makedirs("done", exist_ok=True)

for name in ["a.txt", "b.txt", "c.txt"]:
    open(f"inbox/{name}", "w").close()

shutil.move("inbox/a.txt", "done/a.txt")
shutil.copy2("inbox/b.txt", "done/b.txt")

print("inbox:", os.listdir("inbox"))
print("done: ", os.listdir("done"))

shutil.rmtree("inbox")
shutil.rmtree("done")