items = ["Apple", "Banana", "Orange", "Mango"]

with open("fruits.txt", "w") as f:
    for item in items:
        f.write(item + "\n")

with open("fruits.txt", "r") as f:
    print(f.read())

