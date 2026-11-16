from connect import connect


def main():
    conn = connect()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_database()")
                print("Database:", cur.fetchone()[0])

                cur.execute("""
                    SELECT table_name, column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name IN ('contacts', 'phones', 'groups')
                    ORDER BY table_name, ordinal_position
                """)

                print("\nCURRENT COLUMNS:")
                for table, column, data_type, nullable in cur.fetchall():
                    print(
                        f"{table}.{column} | {data_type} | "
                        f"allows NULL: {nullable}"
                    )

                cur.execute("""
                    SELECT conname, pg_get_constraintdef(oid)
                    FROM pg_constraint
                    WHERE conrelid = 'public.contacts'::regclass
                    ORDER BY conname
                """)

                print("\nCONTACTS CONSTRAINTS:")
                for name, definition in cur.fetchall():
                    print(f"{name}: {definition}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()