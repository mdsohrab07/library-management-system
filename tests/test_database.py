import sqlite3

import pytest

import database


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    """Use a separate SQLite database for each test."""
    database_path = tmp_path / "test-library.db"
    monkeypatch.setattr(database, "DATABASE_PATH", database_path)
    database.init_db()
    return database_path


def test_init_db_creates_books_table(temporary_database):
    with sqlite3.connect(temporary_database) as connection:
        table = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name = 'books'"
        ).fetchone()

    assert table == ("books",)


def test_add_book_inserts_record(temporary_database):
    book_id = database.add_book(
        "Clean Code", "Robert C. Martin", "Programming", 3
    )

    assert book_id == 1
    assert database.get_all_books() == [
        (1, "Clean Code", "Robert C. Martin", "Programming", 3)
    ]


def test_get_all_books_returns_all_rows(temporary_database):
    database.add_book("Book One", "Author One", "Mathematics", 2)
    database.add_book("Book Two", "Author Two", "Electronics", 4)

    assert database.get_all_books() == [
        (1, "Book One", "Author One", "Mathematics", 2),
        (2, "Book Two", "Author Two", "Electronics", 4),
    ]


def test_get_total_books_returns_zero_for_empty_database(temporary_database):
    assert database.get_total_books() == 0


def test_get_total_books_returns_sum_after_inserts(temporary_database):
    database.add_book("Book One", "Author One", "Programming", 2)
    database.add_book("Book Two", "Author Two", "Data Science", 5)

    assert database.get_total_books() == 7


def test_get_most_available_book_returns_empty_for_empty_database(
    temporary_database,
):
    assert database.get_most_available_book() == []


def test_get_most_available_book_returns_book_with_highest_stock(
    temporary_database,
):
    database.add_book("Low Stock", "Author One", "Programming", 2)
    database.add_book("High Stock", "Author Two", "Data Science", 7)

    assert database.get_most_available_book() == [
        (2, "High Stock", "Author Two", "Data Science", 7)
    ]


def test_get_most_available_book_returns_all_ties(temporary_database):
    database.add_book("First Tie", "Author One", "Programming", 7)
    database.add_book("Second Tie", "Author Two", "Mathematics", 7)
    database.add_book("Lower Stock", "Author Three", "Management", 1)

    assert database.get_most_available_book() == [
        (1, "First Tie", "Author One", "Programming", 7),
        (2, "Second Tie", "Author Two", "Mathematics", 7),
    ]


def test_get_category_summary_groups_and_sums_copies(temporary_database):
    database.add_book("Programming One", "Author One", "Programming", 2)
    database.add_book("Programming Two", "Author Two", "Programming", 5)
    database.add_book("AI Book", "Author Three", "Artificial Intelligence", 4)

    assert database.get_category_summary() == [
        ("Artificial Intelligence", 4),
        ("Programming", 7),
    ]


def test_add_book_rejects_negative_copies(temporary_database):
    with pytest.raises(sqlite3.IntegrityError):
        database.add_book("Invalid Book", "Author", "Programming", -1)

    assert database.get_all_books() == []
