from pathlib import Path
import os

file_path = Path(input("Enter the file path to delete: "))

if not file_path.exists():
    print("The specified path does not exist.")

elif not file_path.is_file():
    print("The specified path is not a file.")

elif not os.access(file_path.parent, os.W_OK):
    print("You do not have permission to delete this file.")

else:
    confirmation = input("Are you sure you want to delete it? (yes/no): ")

    if confirmation.lower() == "yes":
        file_path.unlink()
        print("The file was deleted successfully.")
    else:
        print("Deletion was cancelled.")