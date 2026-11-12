# ABC Engineering College Library Management System

A simple web-based Library Management System for ABC Engineering College.
Librarians can record books, view the collection, and review inventory
statistics without maintaining spreadsheets manually.

## Features

- Add books with title, author, category, and available-copy count.
- View all books in a searchable, readable data table.
- Display the total number of available copies.
- Identify the book or books with the highest available stock.
- Summarize available copies by category with a table and bar chart.
- Persist records in a local SQLite database.
- Validate required text fields and non-negative copy counts.

## Tech Stack

- **Python**
- **Streamlit** for the web interface
- **SQLite** for persistent storage
- **pytest** for automated tests

## Folder Structure

```text
library management course/
├── app.py                  # Streamlit application
├── database.py             # SQLite connection, schema, and queries
├── library.db              # Runtime database (created locally)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Ignored files and folders
├── docs/
│   ├── database_design.md  # Database design and SQL schema
│   ├── requirements.md     # Software requirements specification
│   └── test_cases.md       # Automated and manual test checklist
└── tests/
    └── test_database.py    # Database unit tests
```

## Setup

### 1. Clone the repository

```powershell
git clone <repository-url>
cd "library management course"
```

Replace `<repository-url>` with the URL of the project repository.

### 2. Create a virtual environment

```powershell
py -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
venv\Scripts\activate
```

If PowerShell blocks activation, run PowerShell as the current user and
configure its execution policy as appropriate for your environment.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the App

From the project directory with the virtual environment activated:

```powershell
streamlit run app.py
```

Streamlit will print a local URL. Open that URL in a browser and use the
sidebar to select Add Book, View Books, Total Books, Most Available Book, or
Category Summary.

## Run Tests

Run the automated database tests with:

```powershell
python -m pytest tests/test_database.py -q
```

The tests use temporary SQLite databases and do not modify the runtime
`library.db` file.

## Database Schema

The application stores data in `library.db`, using one `books` table:

```sql
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author_name TEXT NOT NULL,
    category TEXT NOT NULL,
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0)
);
```

The complete database design is documented in
[docs/database_design.md](docs/database_design.md).

## Sample Screenshots

Add screenshots to this section as the interface is demonstrated:

```text
![Add Book page](docs/screenshots/add-book.png)
![View Books page](docs/screenshots/view-books.png)
![Category Summary page](docs/screenshots/category-summary.png)
```

## Future Enhancements

- Issue and return book workflows with transaction history.
- Search and filtering by title, author, or category.
- User login and role-based access for librarians and administrators.
- Edit and delete book records.
- Import and export of inventory data.
- Deployment on a shared college server.
