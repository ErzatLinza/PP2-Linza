import re

text = input()
result = re.split("[A-Z]", text)
result = [word for word in result if word]

print(result)