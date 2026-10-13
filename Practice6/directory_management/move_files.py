import os
import shutil

source_file= os.path.join("my_folder", "sample.txt")
destination_folder = "moved_files"

#create the destination directory
os.makedirs(destination_folder, exist_ok = True)

#move the file
destination_file= os.path.join(destination_folder, "sample.txt")

if os.path.exists(source_file):
    shutil.move(source_file, destination_file)
    print(f"File moved to '{destination_file}'. ")
else:
    print(f"Source file '{source_file}' does not exit")