words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

students = [("Emil", 25),("Tobias", 22),("Linus", 28)]
students_sorted = sorted(students, key = lambda x : x[1])
print(students_sorted)