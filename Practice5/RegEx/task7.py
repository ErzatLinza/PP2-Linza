import re
text = input()

result = re.sub(
    "_([a-z])",
    lambda match : match.group(1).upper(),
    text
)

print(result)