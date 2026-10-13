file_name = "sample.txt"

#1task write sample
with open(file_name, "w") as f:
    f.write("Hello world!\n")
    f.write("This is sample data.\n")

print("Sample data was written to", file_name)

#3task append new line
with open(file_name, "a") as f:
    f.write("This line was appending.\n")
    f.write("Python file handling is useful.\n")

with open(file_name, "r") as f:
    print(f.read())