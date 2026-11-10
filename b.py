import os
import shutil
from pathlib import Path

with open("names.txt", "w") as file:
    file.write("Aruzhan\n")
    file.write("Ali\n")
    file.write("Dana\n")
    file.write("Miras\n")
    file.write("Amina\n")

with open("scores.txt", "w") as file:
    file.write("85\n")
    file.write("92\n")
    file.write("78\n")
    file.write("88\n")
    file.write("95\n")

with open("names.txt", "r") as f:
    names = [name.strip() for name in f.readlines()]

with open("scores.txt", "r") as f:
    scores = list(map(int, f.readlines()))

for name, score in zip(names, scores):
    print(f"{name}: {score}")

highest_score = max(scores)
lowest_score = min(scores)

highest_position = scores.index(highest_score)
lowest_position = scores.index(lowest_score)

print("highest", names[highest_position], highest_score)
print("Lowest: ", names[lowest_position], lowest_score)