from pathlib import Path
import psycopg2
from connect import connect

def install_sql(conn):
    with conn:
        with conn.cursor() as cur:
            for filename in (
                "schema.sql",
                "functions.sql",
                "procedures.sql"
            ):
                path = Path(__file__).with_name(filename)
                sql = path.read_text(encoding="utf-8")
                cur.execute(sql)

def search_contacts(conn, pattern):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_by_pattern(%s)",
                (pattern,)
            )
            return cur.fetchall()
        
def upsert_contact(conn,username, phone, first_name = None, surname = None):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s,%s)",
                (username, phone, first_name, surname)
            )

def insert_many_contacts(conn, username, phones):
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_many_contacts(%s::text[], %s::text[], %s::jsonb)",
                (username, phones, "[]")
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
        
def show_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    print("ID | Username | First name | Surname | Phone")

    for row in rows:
        print(" | ".join(str(value) for value in row))

def main():
    try:
        conn = connect()
    except psycopg2.Error as error:
        print("Connection failed: ", error)
        return
    
    try:
        install_sql(conn)
        print("PhoneBook is ready!")

        while True:
            print("\n1. Search contacts")
            print("2. Add or update a contact")
            print("3. Add many contacts")
            print("4. Show a page")
            print("5. Delete a contact")
            print("0. Exit")
            
            choice = input("Choose: ").strip()

            try:
                if choice == "0":
                    break

                elif choice == "1":
                    pattern = input("Part of name, surname or phone: ")
                    rows = search_contacts(conn, pattern)
                    show_contacts(rows)

                elif choice == "2":
                    username = input("Username: ")
                    phone = input("Phone: ")

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

                    print(f"Accepted entries: {count - len(incorrect)}")
                    print(f"Rejected entries: {len(incorrect)}")

                    for entry in incorrect:
                        print(
                            f"Position {entry['position']}: "
                            f"{entry['username']} | "
                            f"{entry['phone']} | "
                            f"{entry['reason']}"
                        )

                elif choice == "4":
                    limit = int(input("How many contacts to show? "))
                    offset = int(input("How many contacts to skip? "))

                    rows = get_page(conn, limit, offset)
                    show_contacts(rows)

                
                elif choice == "5":
                    field = input(
                        "Delete by username or phone: "
                    ).strip()

                    value = input("Exact value: ")
                    deleted = delete_contact(conn, field, value)

                    if deleted == 0:
                        print("Contact not found.")
                    else:
                        print(f"Deleted {deleted} contact(s).")

                else:
                    print("Choose a number from 0 to 5.")

            except psycopg2.Error as error:
                print(
                    "Database error:",
                    error.diag.message_primary or str(error)
                )

            except ValueError as error:
                print("Input error:", error)

    except (psycopg2.Error, OSError) as error:
        print("Setup failed:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

                    
