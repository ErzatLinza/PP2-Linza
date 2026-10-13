#enumerate() gives each list item an index
subjects = ["Python", "Databases", "Cloud Computing"]

print("Subjects: ")
for position, subject in enumerate(subjects, start = 1):
    print(position, subject)

#zip() pairs items from two or more lists
students = ["Ali", "Amina", "Dana"]
scores = [85, 92, 78]

print("\nStudents and scores")
for student, score in zip(students, scores):
    print(student, "-", score)

#enumerate and zip can be used together
print("\nNumbered result: ")
for position, (student, score) in enumerate(zip(students, scores), start = 1):
    print(position, student, "-", score)

# More type checking and conversions.
score_as_text = str(scores[0])
scores_as_tuple = tuple(scores)
subjects_as_set = set(subjects)

print("\nType of score_as_text:", type(score_as_text))
print("Scores converted to tuple:", scores_as_tuple)
print("Subjects converted to set:", subjects_as_set)
