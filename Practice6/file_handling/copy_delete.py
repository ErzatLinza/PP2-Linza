import shutil
import os

file_name = "sample.txt"
backup_name = "sample_backup.txt"

#4.copy the original
if os.path.exists(file_name):
    shutil.copy(file_name, backup_name)
    print("Backup created: ", backup_name)
else:
    print(file_name, "does not exist. ")

#5. delete files safely

if os.path.exists(file_name):
    os.remove(file_name)
    print(file_name,"was deleted.")

if os.path.exists(backup_name):
    os.remove(backup_name)
    print(backup_name, "was deleted.")