import os

path = input("Enter a directory path: ")

if os.path.isdir(path):
    items = os.listdir(path)

    directories = [
        item for item in items
        if os.path.isdir(os.path.join(path, item))
    ]

    files = [
        item for item in items
        if os.path.isfile(os.path.join(path, item))
    ]

    print("\nDirectories:")
    for directory in directories:
        print(directory)

    print("\nFiles: ")
    for file in files:
        print(file)

    print("\nAll directories and files: ")
    for item in items:
        print(item)

else:
    print("The specified directory does not exist.")