import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("library.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the library.db SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


def init_db() -> None:
    """Create the books table if it does not already exist."""
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL,
                author_name TEXT NOT NULL,
                category TEXT NOT NULL,
                available_copies INTEGER NOT NULL CHECK (available_copies >= 0)
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    """Create the books table using the legacy initialization name."""
    init_db()


def add_book(title: str, author: str, category: str, copies: int) -> int:
    """Add a book and return its generated book ID."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO books (
                book_title, author_name, category, available_copies
            )
            VALUES (?, ?, ?, ?)
            """,
            (title, author, category, copies),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_all_books() -> list[tuple[int, str, str, str, int]]:
    """Return all books ordered by their book ID."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            ORDER BY book_id
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


def get_total_books() -> int:
    """Return the total number of available copies, or zero when empty."""
    connection = get_connection()
    try:
        result = connection.execute(
            "SELECT COALESCE(SUM(available_copies), 0) FROM books"
        ).fetchone()
        return int(result[0])
    finally:
        connection.close()


def get_most_available_book() -> list[tuple[int, str, str, str, int]]:
    """Return all books tied for the highest number of available copies."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT book_id, book_title, author_name, category, available_copies
            FROM books
            WHERE available_copies = (
                SELECT MAX(available_copies) FROM books
            )
            ORDER BY book_id
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


def get_category_summary() -> list[tuple[str, int]]:
    """Return total available copies grouped by category."""
    connection = get_connection()
    try:
        cursor = connection.execute(
            """
            SELECT category, SUM(available_copies) AS total_copies
            FROM books
            GROUP BY category
            ORDER BY category
            """
        )
        return cursor.fetchall()
    finally:
        connection.close()


if __name__ == "__main__":
    init_db()
