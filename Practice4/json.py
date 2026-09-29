import sys
from pathlib import Path

# Prevent json.py from conflicting with Python's built-in json module
current_folder = str(Path(__file__).parent.resolve())

if current_folder in sys.path:
    sys.path.remove(current_folder)

import json

file_path = Path(__file__).parent / "sample-data.json"

with open(file_path, "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print(f"{'-' * 50} {'-' * 20} {'-' * 8} {'-' * 6}")

for interface in data["imdata"]:
    attributes = interface["l1PhysIf"]["attributes"]

    print(
        f"{attributes['dn']:<50} "
        f"{attributes['descr']:<20} "
        f"{attributes['speed']:<8} "
        f"{attributes['mtu']:<6}"
    )