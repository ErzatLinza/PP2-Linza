from pathlib import Path
import string

for letter in string.ascii_uppercase:
    filename = Path(letter + ".txt")
    filename.write_text(
        "This is file" + filename.name,
    )

