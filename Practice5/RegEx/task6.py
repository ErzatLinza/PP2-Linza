import re


# 6. Replace spaces, commas, and dots with colons
text = input("Enter a string: ")

result = re.sub("[ ,\.]", ":", text)
print(result)