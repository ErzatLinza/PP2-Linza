import os

with open("words.txt", "x") as f:
    f.write("apple\n")
    f.write("computer\n")
    f.write("book\n")
    f.write("python\n")
    f.write("table\n")
    f.write("university\n")
    f.write("student\n")
    f.write("pen\n")

with open("words.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]

filtered_words = list(filter(lambda word: len(word)>5, words))

with open("long_words.txt", "w") as f:
    for word in filtered_words:
        f.write(word+"\n")

with open("long_words.txt", "r") as f:
    print(f.read())

if os.path.exists("words.txt"):
    os.remove("words.txt")



