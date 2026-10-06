import re

text = input()

result = re.sub("(?<!^)(?=[A-Z])", "_", text).lower()
print(result)

result = re.sub("([A-Z])", "_\1", text).lower().strip("_")
print(result)