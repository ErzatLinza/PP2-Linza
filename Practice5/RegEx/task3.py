import re


# 3. Lowercase letters joined with an underscore
text = input("Enter a string: ")

results = re.findall("[a-z]+_[a-z]+", text)
print(results)