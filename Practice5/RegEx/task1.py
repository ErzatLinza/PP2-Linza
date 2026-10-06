import re

text = input()

x = re.fullmatch("ab*", text)
print(x)

if x :
    print("Match")
else: 
    print("Not match")
