
import csv
import sqlite3
from pathlib import Path

CSV_FILE = Path(__file__).with_name("users.csv")
DB_FILE = Path(__file__).with_name("users.db")


def create_table(connection):
    """Create the users table if it does not exist."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)


def import_users(connection):
    """Read users from CSV and insert valid records."""
    inserted = 0
    skipped = 0

    with CSV_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"name", "email"}.issubset(
            reader.fieldnames
        ):
            raise ValueError("CSV must contain name and email columns.")

        for row in reader:
            name = (row.get("name") or "").strip()
            email = (row.get("email") or "").strip()

            if not name or not email or "@" not in email:
                print(f"Skipping invalid record: {row}")
                skipped += 1
                continue

            cursor = connection.execute("""
                INSERT INTO users (name, email)
                VALUES (?, ?)
                ON CONFLICT(email) DO NOTHING
            """, (name, email))

            if cursor.rowcount == 1:
                inserted += 1
            else:
                print(f"Skipping duplicate email: {email}")
                skipped += 1

    return inserted, skipped


def display_users(connection):
    """Display the records stored in SQLite."""
    rows = connection.execute("""
        SELECT id, name, email
        FROM users
        ORDER BY id
    """).fetchall()

    print("\nUsers stored in the database:")
    for user_id, name, email in rows:
        print(f"{user_id}. {name} - {email}")

    print(f"\nTotal users in database: {len(rows)}")


def main():
    try:
        with sqlite3.connect(DB_FILE) as connection:
            create_table(connection)
            inserted, skipped = import_users(connection)

            print(f"New users inserted: {inserted}")
            print(f"Records skipped: {skipped}")

            display_users(connection)

    except FileNotFoundError:
        print(f"CSV file not found: {CSV_FILE}")

    except (OSError, csv.Error, sqlite3.Error, ValueError) as error:
        print(f"Import failed: {error}")


if __name__ == "__main__":
    main()