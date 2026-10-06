import re


# 4. One uppercase letter followed by lowercase letters
text = input("Enter a string: ")

results = re.findall("[A-Z][a-z]+", text)
print(results)