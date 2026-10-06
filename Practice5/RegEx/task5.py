import re


# 5. Starts with 'a' and ends with 'b'
text = input("Enter a string: ")

if re.fullmatch("a.*b", text):
    print("Match")
else:
    print("No match")