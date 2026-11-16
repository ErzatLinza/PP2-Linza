from pathlib import Path
from datetime import date
import csv
import json

import psycopg2
from connect import connect


# ---------- Database setup ----------

def install_sql(conn):
    with conn:
        with conn.cursor() as cur:
            for filename in (
                "schema.sql",
                "functions.sql",
                "procedures.sql"
            ):
                path = Path(__file__).with_name(filename)
                cur.execute(path.read_text(encoding="utf-8"))


# ---------- Existing operations ----------

def search_contacts(conn, pattern):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (pattern,)
            )
            return cur.fetchall()


def upsert_contact(
    conn, username, phone, first_name=None, surname=None
):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s, %s)",
                (username, phone, first_name, surname)
            )


def insert_many_contacts(conn, usernames, phones):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CALL insert_many_contacts(
                    %s::text[], %s::text[], %s::jsonb
                )
                """,
                (usernames, phones, "[]")
            )
            return cur.fetchone()[0]


def get_page(conn, limit, offset):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )
            return cur.fetchall()


def delete_contact(conn, field, value):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL delete_contact(%s, %s, %s)",
                (field, value, 0)
            )
            return cur.fetchone()[0]


# ---------- New contact operations ----------

def add_phone(conn, username, phone, phone_type):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL add_phone(%s, %s, %s)",
                (username, phone, phone_type)
            )


def move_to_group(conn, username, group_name):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL move_to_group(%s, %s)",
                (username, group_name)
            )


def filter_by_group(conn, group_name):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.id, c.username, c.first_name,
                       c.surname, c.phone, c.email
                FROM contacts AS c
                JOIN groups AS g ON c.group_id = g.id
                WHERE g.name = %s
                ORDER BY c.id
                """,
                (group_name,)
            )
            return cur.fetchall()


def update_contact_details(conn, username, email, birthday):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE contacts
                SET email = COALESCE(%s, email),
                    birthday = COALESCE(%s, birthday)
                WHERE username = %s
                """,
                (email, birthday, username)
            )
            return cur.rowcount


def get_sorted_contacts(conn, sort_by):
    sort_options = {
        "name": "c.first_name, c.surname, c.id",
        "birthday": "c.birthday NULLS LAST, c.id",
        "added": "c.created_at NULLS LAST, c.id"
    }

    if sort_by not in sort_options:
        raise ValueError("Choose name, birthday or added.")

    # Only predefined SQL expressions are inserted into the query.
    order = sort_options[sort_by]

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT c.id, c.username, c.first_name,
                       c.surname, c.phone, c.email,
                       c.birthday, c.created_at
                FROM contacts AS c
                ORDER BY {order}
                """
            )
            return cur.fetchall()


# ---------- Display and pagination ----------

def show_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    headings = "ID | Username | First name | Surname | Phone"

    if len(rows[0]) >= 6:
        headings += " | Email"

    if len(rows[0]) == 8:
        headings += " | Birthday | Date added"

    print(headings)

    for row in rows:
        print(
            " | ".join(
                str(value) if value is not None else "-"
                for value in row
            )
        )


def browse_contacts(conn):
    page_size = int(input("Contacts per page: "))

    if page_size <= 0:
        raise ValueError("Page size must be positive.")

    offset = 0

    while True:
        rows = get_page(conn, page_size, offset)

        print(f"\nPage {offset // page_size + 1}")
        show_contacts(rows)

        command = input("next / prev / quit: ").strip().lower()

        if command == "quit":
            break

        elif command == "next":
            next_rows = get_page(
                conn, page_size, offset + page_size
            )

            if next_rows:
                offset += page_size
            else:
                print("You are on the last page.")

        elif command == "prev":
            if offset == 0:
                print("You are on the first page.")
            else:
                offset -= page_size

        else:
            print("Enter next, prev or quit.")


# ---------- JSON export ----------

def export_contacts(conn, filename):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT jsonb_build_object(
                    'username', c.username,
                    'first_name', c.first_name,
                    'surname', c.surname,
                    'phone', c.phone,
                    'email', c.email,
                    'birthday', c.birthday,
                    'created_at', c.created_at,
                    'group', g.name,
                    'phones', COALESCE(
                        (
                            SELECT jsonb_agg(
                                jsonb_build_object(
                                    'phone', p.phone,
                                    'type', p.type
                                )
                                ORDER BY p.id
                            )
                            FROM phones AS p
                            WHERE p.contact_id = c.id
                        ),
                        '[]'::JSONB
                    )
                )
                FROM contacts AS c
                LEFT JOIN groups AS g ON c.group_id = g.id
                ORDER BY c.id
            """)

            contacts = [row[0] for row in cur.fetchall()]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            contacts,
            file,
            ensure_ascii=False,
            indent=4
        )

    return len(contacts)


# ---------- Shared import logic ----------

def import_contact_records(conn, contacts):
    if not isinstance(contacts, list):
        raise ValueError("Import data must be a list of contacts.")

    imported = 0
    skipped = 0

    # All database changes from this import share one transaction.
    with conn:
        with conn.cursor() as cur:
            for contact in contacts:
                if not isinstance(contact, dict):
                    raise ValueError("Each contact must be an object.")

                username = contact.get("username")
                phone = contact.get("phone")

                if not isinstance(username, str) or not username.strip():
                    raise ValueError("Each contact needs a username.")

                if not isinstance(phone, str) or not phone.strip():
                    raise ValueError("Each contact needs an original phone.")

                username = username.strip()
                phone = phone.strip()

                cur.execute(
                    "SELECT id FROM contacts WHERE username = %s",
                    (username,)
                )
                existing = cur.fetchone()

                if existing:
                    while True:
                        action = input(
                            f"{username} already exists. "
                            "skip / overwrite: "
                        ).strip().lower()

                        if action in ("skip", "overwrite"):
                            break

                        print("Enter skip or overwrite.")

                    if action == "skip":
                        skipped += 1
                        continue

                first_name = contact.get("first_name") or username
                surname = contact.get("surname") or ""
                email = contact.get("email")
                group_name = contact.get("group") or "Other"

                for label, value in (
                    ("first_name", first_name),
                    ("surname", surname),
                    ("group", group_name)
                ):
                    if not isinstance(value, str):
                        raise ValueError(f"{label} must be text.")

                if email is not None and not isinstance(email, str):
                    raise ValueError("Email must be text or null.")

                birthday_text = contact.get("birthday")

                if birthday_text is not None and not isinstance(
                    birthday_text, str
                ):
                    raise ValueError(
                        "Birthday must be YYYY-MM-DD text or null."
                    )

                birthday = (
                    date.fromisoformat(birthday_text)
                    if birthday_text else None
                )

                phones = contact.get("phones", [])

                if not isinstance(phones, list):
                    raise ValueError("phones must be a list.")

                for item in phones:
                    if not isinstance(item, dict):
                        raise ValueError("Each phone must be an object.")

                    if not isinstance(item.get("phone"), str):
                        raise ValueError("Each phone needs a text number.")

                    if item.get("type") not in (
                        "home", "work", "mobile"
                    ):
                        raise ValueError(
                            "Phone type must be home, work or mobile."
                        )

                # Use the cursor directly so helper functions do not
                # commit individual operations during the import.
                cur.execute(
                    "CALL upsert_contact(%s, %s, %s, %s)",
                    (username, phone, first_name, surname)
                )

                cur.execute(
                    """
                    UPDATE contacts
                    SET email = %s, birthday = %s
                    WHERE username = %s
                    RETURNING id
                    """,
                    (email, birthday, username)
                )
                contact_id = cur.fetchone()[0]

                cur.execute(
                    "CALL move_to_group(%s, %s)",
                    (username, group_name)
                )

                # Overwrite replaces the contact's phone list.
                cur.execute(
                    "DELETE FROM phones WHERE contact_id = %s",
                    (contact_id,)
                )

                for item in phones:
                    cur.execute(
                        "CALL add_phone(%s, %s, %s)",
                        (username, item["phone"], item["type"])
                    )

                # Ensure the original phone is included.
                # If already imported, its existing type is preserved.
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (username, phone, "mobile")
                )

                imported += 1

    return imported, skipped


# ---------- JSON import ----------

def import_contacts_json(conn, filename):
    with open(filename, "r", encoding="utf-8-sig") as file:
        contacts = json.load(file)

    return import_contact_records(conn, contacts)


# ---------- CSV import ----------

def import_contacts_csv(conn, filename):
    contacts = {}

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"username", "first_name", "phone"}

        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV needs username, first_name and phone columns."
            )

        for row in reader:
            if None in row or any(
                value is None for value in row.values()
            ):
                raise ValueError(
                    "Wrong number of CSV fields near "
                    f"line {reader.line_num}."
                )

            username = row["username"].strip()
            phone = row["phone"].strip()

            details = {
                "username": username,
                "first_name": row["first_name"].strip(),
                "surname": row.get("surname", "").strip(),
                "email": row.get("email", "").strip() or None,
                "birthday": row.get("birthday", "").strip() or None,
                "group": row.get("group", "").strip() or "Other"
            }

            phone_entry = {
                "phone": phone,
                "type": (
                    row.get("phone_type", "").strip().lower()
                    or "mobile"
                )
            }

            if username not in contacts:
                contacts[username] = {
                    **details,
                    "phone": phone,
                    "phones": []
                }
            else:
                for field, value in details.items():
                    if contacts[username][field] != value:
                        raise ValueError(
                            f"Conflicting {field} values for {username}."
                        )

            contacts[username]["phones"].append(phone_entry)

    return import_contact_records(conn, list(contacts.values()))


# ---------- Main menu ----------

def main():
    try:
        conn = connect()
    except psycopg2.Error as error:
        print("Connection failed:", error)
        return

    try:
        install_sql(conn)
        print("PhoneBook is ready!")

        while True:
            print("\n1. Search names, email or any phone")
            print("2. Add or update a contact")
            print("3. Add many contacts")
            print("4. Browse contacts: next / prev / quit")
            print("5. Delete a contact")
            print("6. Add an extra phone")
            print("7. Move contact to a group")
            print("8. Filter contacts by group")
            print("9. Set email and birthday")
            print("10. Show sorted contacts")
            print("11. Export contacts to JSON")
            print("12. Import contacts from JSON")
            print("13. Import contacts from CSV")
            print("0. Exit")

            choice = input("Choose: ").strip()

            try:
                if choice == "0":
                    break

                elif choice == "1":
                    pattern = input(
                        "Part of name, email or phone: "
                    )
                    show_contacts(search_contacts(conn, pattern))

                elif choice == "2":
                    username = input("Username: ").strip()
                    phone = input("Phone: ").strip()

                    first_name = input(
                        "First name (Enter to keep/default): "
                    ).strip() or None

                    surname = input(
                        "Surname (Enter to keep/default): "
                    ).strip() or None

                    upsert_contact(
                        conn, username, phone, first_name, surname
                    )
                    print("Contact saved!")

                elif choice == "3":
                    count = int(input("Number of contacts: "))

                    if count < 0:
                        raise ValueError("Count cannot be negative.")

                    usernames = []
                    phones = []

                    for i in range(count):
                        print(f"\nContact {i + 1}")
                        usernames.append(input("Username: "))
                        phones.append(input("Phone: "))

                    incorrect = insert_many_contacts(
                        conn, usernames, phones
                    )

                    print(
                        f"Accepted entries: {count - len(incorrect)}"
                    )
                    print(f"Rejected entries: {len(incorrect)}")

                    for entry in incorrect:
                        print(
                            f"Position {entry['position']}: "
                            f"{entry['username']} | "
                            f"{entry['phone']} | "
                            f"{entry['reason']}"
                        )

                elif choice == "4":
                    browse_contacts(conn)

                elif choice == "5":
                    field = input(
                        "Delete by username or phone: "
                    ).strip()

                    value = input("Exact value: ").strip()
                    deleted = delete_contact(conn, field, value)

                    if deleted == 0:
                        print("Contact not found.")
                    else:
                        print(f"Deleted {deleted} contact(s).")

                elif choice == "6":
                    username = input(
                        "Existing username: "
                    ).strip()

                    phone = input(
                        "New phone number: "
                    ).strip()

                    phone_type = input(
                        "Phone type (home/work/mobile): "
                    ).strip()

                    add_phone(conn, username, phone, phone_type)
                    print(
                        "Phone added, or already exists "
                        "for this contact."
                    )

                elif choice == "7":
                    username = input(
                        "Existing username: "
                    ).strip()

                    group_name = input(
                        "Group (Family/Work/Friend/Other "
                        "or a new name): "
                    ).strip()

                    move_to_group(conn, username, group_name)
                    print(f"Contact moved to {group_name}.")

                elif choice == "8":
                    group_name = input("Group name: ").strip()

                    show_contacts(
                        filter_by_group(conn, group_name)
                    )

                elif choice == "9":
                    username = input(
                        "Existing username: "
                    ).strip()

                    email = input(
                        "Email (Enter to keep current): "
                    ).strip() or None

                    birthday_text = input(
                        "Birthday YYYY-MM-DD "
                        "(Enter to keep current): "
                    ).strip()

                    birthday = (
                        date.fromisoformat(birthday_text)
                        if birthday_text else None
                    )

                    updated = update_contact_details(
                        conn, username, email, birthday
                    )

                    if updated == 0:
                        print("Contact not found.")
                    else:
                        print("Contact details updated.")

                elif choice == "10":
                    sort_by = input(
                        "Sort by name, birthday or added: "
                    ).strip().lower()

                    show_contacts(
                        get_sorted_contacts(conn, sort_by)
                    )

                elif choice == "11":
                    filename = Path(__file__).with_name(
                        "contacts_export.json"
                    )

                    count = export_contacts(conn, filename)

                    print(f"Exported {count} contacts.")
                    print(f"File: {filename}")

                elif choice == "12":
                    filename = input(
                        "JSON path "
                        "(Enter for contacts_export.json): "
                    ).strip()

                    filename = (
                        Path(filename).expanduser()
                        if filename
                        else Path(__file__).with_name(
                            "contacts_export.json"
                        )
                    )

                    imported, skipped = import_contacts_json(
                        conn, filename
                    )

                    print(
                        f"Imported: {imported}; skipped: {skipped}"
                    )

                elif choice == "13":
                    filename = input(
                        "CSV path (Enter for contacts.csv): "
                    ).strip()

                    filename = (
                        Path(filename).expanduser()
                        if filename
                        else Path(__file__).with_name(
                            "contacts.csv"
                        )
                    )

                    imported, skipped = import_contacts_csv(
                        conn, filename
                    )

                    print(
                        f"Imported: {imported}; skipped: {skipped}"
                    )

                else:
                    print("Choose a number from 0 to 13.")

            except psycopg2.Error as error:
                print(
                    "Database error:",
                    error.diag.message_primary or str(error)
                )

            except (ValueError, csv.Error) as error:
                print("Input/file format error:", error)

            except (OSError, UnicodeError) as error:
                print("File error:", error)

    except (psycopg2.Error, OSError, UnicodeError) as error:
        print("Setup failed:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")