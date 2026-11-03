from connect import connect 
import psycopg2
import csv
from pathlib import Path

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                    )
        """)

    conn.commit()
    print("Contact table is ready!")

def insert_contact(conn):
    username = input("Username: ").strip()
    first_name = input("First name: ").strip()
    phone = input("Phone: ").strip()

    if not username or not first_name or not phone:
        print("Please fill in all fields")
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contacts(username, first_name, phone)
                VALUES(%s, %s, %s)
            """, (username, first_name, phone)
            )

        conn.commit()
        print("Contact saved!")

    except psycopg2.Error as error:
        conn.rollback()
        print("Could not save contact: ", error)

def show_contacts(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, username, first_name, phone
            FROM contacts
            ORDER BY id
         """
        )

        contacts = cur.fetchall()

    if not contacts:
        print("No contacts found. ")
        return
    
    for contact in contacts:
        print(contact)

def import_csv(conn):
    filename = Path(__file__).with_name("contacts.csv")

    try:
        with open(filename, newline="", encoding = "utf-8-sig") as file:
            reader = csv.DictReader(file)

            contacts = [
                (row["username"], row["first_name"], row["phone"])
                for row in reader
            ]
            
        with conn.cursor() as cur:
            cur.executemany(
                """ 
                INSERT INTO contacts (username, first_name, phone)
                VALUES (%s, %s, %s)

             """, contacts
            )

    except psycopg2.Error as error:
        conn.rollback()
        print("Import failed. No new contacts were saved:", error)

    except (OSError, KeyError, UnicodeError, csv.Error) as error:
        print("Could not read CSV:", error)

def update_contact(conn):
    username = input("Username to update: ").strip()
    field = input("Change first name or phone? (name/phone): ").strip()

    if field == "name":
        query = """
            UPDATE contacts
            SET first_name = %s
            WHERE username = %s
     """
        
    elif field == "phone":
        query = """
            UPDATE contacts
            SET phone = %s
            WHERE username = %s
     """
        
    else:
        print("Please choose name or phone. ")
        return
    
    new_value = input("New value: ").strip()

    if not new_value:
        print("The new value cannot be empty.")

    try:
        with conn.cursor() as cur:
            cur.execute(query, (new_value, username))
            updated = cur.rowcount

        conn.commit()

        if updated == 0:
            print("Username not found")

        else:
            print("Contact updated!")

    except psycopg2.Error as error:
        conn.rollback()
        print("Update failed:", error)

def search_contacts(conn):
    choice = input("Search by name or phone prefix? (name/phone): ").strip()
    value = input("Search text: ").strip()

    if not value:
        print("Please enter search text.")
        return

    if choice == "name":
        query = """
            SELECT id, username, first_name, phone
            FROM contacts
            WHERE first_name ILIKE %s
            ORDER BY id
        """
        pattern = "%" + value + "%"

    elif choice == "phone":
        query = """
            SELECT id, username, first_name, phone
            FROM contacts
            WHERE phone LIKE %s
            ORDER BY id
        """
        pattern = value + "%"

    else:
        print("Please choose name or phone.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(query, (pattern,))
            contacts = cur.fetchall()

        if not contacts:
            print("No contacts found.")
        else:
            for contact in contacts:
                print(contact)

    except psycopg2.Error as error:
        conn.rollback()
        print("Search failed:", error)


def delete_contact(conn):
    choice = input("Delete by username or phone? (username/phone): ").strip()

    if choice == "username":
        query = "DELETE FROM contacts WHERE username = %s"
    elif choice == "phone":
        query = "DELETE FROM contacts WHERE phone = %s"
    else:
        print("Please choose username or phone.")
        return

    value = input("Enter the exact value: ").strip()

    if not value:
        print("The value cannot be empty.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(query, (value,))
            deleted = cur.rowcount

        conn.commit()
        print(f"Deleted {deleted} contact(s).")

    except psycopg2.Error as error:
        conn.rollback()
        print("Delete failed:", error)

if __name__ == "__main__":
    conn = connect()

    try:
        create_table(conn)

        while True:
            print("\n--- PhoneBook ---")
            print("1. Add contact")
            print("2. Import CSV")
            print("3. Show all contacts")
            print("4. Update contact")
            print("5. Search contacts")
            print("6. Delete contact")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                insert_contact(conn)
            elif choice == "2":
                import_csv(conn)
            elif choice == "3":
                show_contacts(conn)
            elif choice == "4":
                update_contact(conn)
            elif choice == "5":
                search_contacts(conn)
            elif choice == "6":
                delete_contact(conn)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Please choose a number from 0 to 6.")

    finally:
        conn.close()