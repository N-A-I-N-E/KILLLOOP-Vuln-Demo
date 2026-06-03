"""Extra SQLi module for static analysis (not only Flask route)."""
import sqlite3


def lookup_user(user_id: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    return cursor.fetchone()
