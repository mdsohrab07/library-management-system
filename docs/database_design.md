# Database Design

## Database overview

The Library Management System uses a single SQLite database file named
`library.db`. The database stores one record for each catalogued book entry.
Each row contains the title, author, category, and number of copies currently
available.

## Entity-relationship description

The database has one entity: **Book**.

- `Book.book_id` uniquely identifies each book record.
- A book has one title, one author, one category, and a non-negative number of
  available copies.
- There are no relationships to other entities in the initial release.
- Duplicate titles are allowed because `book_id` is the only uniqueness
  constraint. This supports separate records for different authors, categories,
  or inventory entries with the same title.

## Schema

```sql
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author_name TEXT NOT NULL,
    category TEXT NOT NULL,
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0)
);
```

## Column definitions

| Column | Type | Constraints | Description |
|---|---|---|---|
| `book_id` | `INTEGER` | Primary key, auto-incremented | Unique identifier for a book record. |
| `book_title` | `TEXT` | Not null | Title of the book. |
| `author_name` | `TEXT` | Not null | Author of the book. |
| `category` | `TEXT` | Not null | Book category selected by the librarian. |
| `available_copies` | `INTEGER` | Not null, must be `>= 0` | Number of copies currently available. |

## Query behavior

- **Total books:** `SUM(available_copies)`, returning `0` for an empty table.
- **Most available book:** all rows whose `available_copies` equals the
  maximum value, including ties.
- **Category summary:** `SUM(available_copies)` grouped by `category`.

All values supplied by the application are passed to SQLite using parameterized
queries.
