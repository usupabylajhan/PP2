import shutil
import os

shutil.copy2("data.txt", "data_backup.txt")
print("Backup created:", os.path.exists("data_backup.txt"))

os.remove("data_backup.txt")
print("Deleted:", not os.path.exists("data_backup.txt"))