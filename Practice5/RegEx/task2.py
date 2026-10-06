import re


# 2. 'a' followed by two or three 'b's
text = input("Enter a string: ")

if re.fullmatch("ab{2,3}", text):
    print("Match")
else:
    print("No match")