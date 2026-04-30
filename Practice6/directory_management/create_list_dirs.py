import os
import glob
import shutil

os.makedirs("project/src/utils", exist_ok=True)
os.makedirs("project/tests", exist_ok=True)
os.makedirs("project/data", exist_ok=True)

open("project/src/main.py", "w").close()
open("project/src/utils/helpers.py", "w").close()
open("project/tests/test_main.py", "w").close()
open("project/data/input.csv", "w").close()

for root, dirs, files in os.walk("project"):
    level = root.count(os.sep)
    print("  " * level + os.path.basename(root) + "/")
    for f in files:
        print("  " * (level + 1) + f)

print("\n.py files:")
for f in glob.glob("project/**/*.py", recursive=True):
    print(" ", f)

shutil.rmtree("project")