import os

path = input("Enter the test file path: ")

if os.path.isfile(path):
    with open(path, "r", encoding= "utf-8") as f:
        line_count = sum(1 for line in f)

    print("Number of lines:", line_count)

else:
    print("The file does not exist.")