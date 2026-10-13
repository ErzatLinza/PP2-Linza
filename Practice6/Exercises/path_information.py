import os

path = input("Enter a file path: ")

if os.path.exists(path):
    directory = os.path.dirname(path)
    filename = os.path.basename(path)

    print("The path exist. ")
    print("Directory portion:", directory)
    print("Filename portion:", filename)
else:
    print("The path does not exist.")