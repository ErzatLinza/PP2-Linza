from pathlib import Path
import shutil

source = Path(input("Enter the source file: "))
destination = Path(input("Enter the destination file: "))

if source.is_file():
    shutil.copy(source, destination)
    print("File copied successfully.")
else:
    print("Source file does not exist.")