import json
import re

data = json.loads(input())

pattern = r"[\w.]+@[\w.]+\.(com|edu)"

for name, email in data.items():
    if re.fullmatch(pattern, email):
        print(name)

for people in data:
    if re.fullmatch(pattern, people["email"]):
        print(people["name"], " - ", people["email"])




import json
import re

with open("json.txt", "r+") as f:
    people = json.load(f)

pattern = r"[0-9]{4}[A-B]{2}"

for person in people:
    if re.fullmatch(pattern, person):
        print(person)



