#!/usr/bin/env python3
"""Inspect the SQLite database schema for DevSaver."""

import sqlite3

DB_FILE = "devsaver.db"

def inspect_database(db_file: str) -> None:
    print(f"\nInspecting database: {db_file}\n")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found.")
        return

    for (table_name,) in tables:
        print(f"Table: {table_name}")

        # List columns for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            col_id, name, col_type, notnull, default, pk = col
            print(f"  - {name} ({col_type})"
                  f"{' PRIMARY KEY' if pk else ''}"
                  f"{' NOT NULL' if notnull else ''}"
                  f"{f' DEFAULT {default}' if default else ''}")
        print()

    conn.close()

if __name__ == "__main__":
    inspect_database(DB_FILE)