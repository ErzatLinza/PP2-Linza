file_name = "sample.txt"

#task2 read and print
try:
    with open(file_name, "r") as f:
        print("File content: ", f.read())

except FileNotFoundError:
    print("The file does not exits.")