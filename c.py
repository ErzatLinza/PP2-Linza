import json
import re

json_data = '''
[
    {"name": "Alice", "email": "alice_123@example.com"},
    {"name": "Bob", "email": "bob.smith@university.edu"},
    {"name": "Charlie", "email": "charlie-test@example.com"},
    {"name": "Diana", "email": "diana@example.org"},
    {"name": "Emma", "email": "emma_2026@college.edu"}
]
'''

people = json.loads(json_data) 

pattern = r"[\w.]+@[\w.]+\.(edu|com)"

selected_people = [
    person
    for person in people
    if re.fullmatch(pattern, person["email"], re.IGNORECASE)
]

for person in selected_people:
    print(person["name"], "-", person["email"])