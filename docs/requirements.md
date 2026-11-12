# Software Requirements Specification

## Library Management System

**Client:** ABC Engineering College  
**Technology stack:** Python, Streamlit, SQLite  
**Document status:** Initial requirements specification

## 1. Project Overview and Objective

ABC Engineering College currently tracks library books and inventory in spreadsheets. This creates a risk of inconsistent records, makes inventory statistics difficult to calculate, and requires manual effort for routine lookups.

The Library Management System (LMS) will be a simple web application for librarians. It will provide a single interface to record books, view the complete collection, and review inventory statistics. The system will use Streamlit for the user interface, Python for application logic, and SQLite for persistent local storage.

### Objective

The objective is to replace spreadsheet-based book tracking with a reliable, easy-to-use application that:

- Maintains a structured record of books and available copies.
- Allows librarians to add and review book records quickly.
- Provides accurate inventory totals and category-level summaries.
- Reduces manual calculation and data-entry errors.

## 2. Scope

### In scope

- Adding a book record.
- Viewing all stored books in a table.
- Calculating total available copies.
- Identifying the book or books with the highest number of available copies.
- Summarizing available copies by category.
- Persisting data in a SQLite database.
- Validating user input before saving records.

### Out of scope

- Student/member accounts and authentication.
- Book issue, return, reservation, or fine management.
- Editing or deleting existing books.
- Barcode scanning.
- Multi-user synchronization or deployment infrastructure.

## 3. Functional Requirements

### FR-01: Add Book

The system shall provide a form that allows a librarian to add a book with:

- **Title**
- **Author**
- **Category**
- **Available copies**

When valid data is submitted, the system shall save one new book record to SQLite and confirm that the record was added successfully.

The category field shall provide these choices:

1. Programming
2. Artificial Intelligence
3. Data Science
4. Mathematics
5. Electronics
6. Management

The system shall not save a record when any validation rule fails. It shall display a clear message identifying the invalid input.

### FR-02: View Books

The system shall display all stored book records in a table. The table shall include, at minimum:

- Title
- Author
- Category
- Available copies

Records shall remain visible after page refreshes because they are stored in SQLite. An empty database shall result in an informative empty-state message rather than an application error.

### FR-03: Total Books

The system shall calculate and display **Total Books** as the sum of available copies across all stored book records.

For an empty database, the total shall be displayed as `0`.

### FR-04: Most Available Book

The system shall identify and display the book or books with the highest available-copies value.

If multiple books share the highest value, the system shall display all tied books rather than selecting one arbitrarily. For an empty database, the system shall display an appropriate message indicating that no books are available.

### FR-05: Category Summary

The system shall calculate and display a category-wise summary of available copies. Each summary row shall contain:

- Category
- Total available copies in that category

The summary shall include categories represented by stored records and shall calculate totals from the current database contents. For an empty database, the system shall display zero totals or an informative empty-state message.

## 4. Non-Functional Requirements

### NFR-01: Usability

- The application shall be usable by librarians with basic computer skills.
- Labels and validation messages shall be clear and understandable.
- The main functions shall be accessible from the primary application page without requiring command-line interaction.
- The book table and inventory statistics shall use readable headings and consistent formatting.

### NFR-02: Performance

- Normal add and read operations shall complete within 2 seconds for a collection of up to 10,000 book records on the target local environment.
- Summary values shall be calculated from current persisted data when displayed or refreshed.
- The application shall avoid unnecessary database operations for a single user action.

### NFR-03: Data Integrity

- Book records shall be stored persistently in SQLite.
- The system shall validate all form inputs before insertion.
- Database queries that include user-entered values shall use parameterized SQL.
- Available copies shall never be stored as a negative value.
- A failed validation or database operation shall not create a partial or invalid book record.
- The database schema shall enforce required fields where supported.

## 5. Input Validation Rules

| Field | Rule |
|---|---|
| Title | Required; must not be empty or whitespace-only. |
| Author | Required; must not be empty or whitespace-only. |
| Category | Required; must be one of Programming, Artificial Intelligence, Data Science, Mathematics, Electronics, or Management. |
| Available copies | Required; must be an integer greater than or equal to `0`. |

The system shall trim leading and trailing whitespace from text values before saving them. Invalid input shall produce a user-visible error and shall not be saved.

## 6. Assumptions and Constraints

### Assumptions

- The application will initially be used by librarians on a trusted local network or local computer.
- A book record represents a title/author/category entry and its current number of available copies.
- Available copies are managed directly by the librarian through the application.
- SQLite is sufficient for the expected initial workload and single-site usage.
- The application will run in an environment with Python and the required packages installed.

### Constraints

- The implementation shall use Python, Streamlit, and SQLite.
- The initial system shall not require an external database server.
- The initial release shall not include authentication or role-based access control.
- The system shall support the defined category list; adding categories requires a requirements or configuration update.
- The initial release is intended for simple local or limited internal use, not high-concurrency operation.

## 7. Edge Cases and Expected Behavior

| Edge case | Expected behavior |
|---|---|
| Empty database | Display total available copies as `0`, show an informative empty-state message for the book list, and indicate that no most-available book exists. |
| Duplicate titles | Allow the records unless a future business rule prohibits duplicates. Each entry remains a separate record so different authors, categories, or inventory counts can be represented. |
| Tie for most available book | Display every book whose available-copies value equals the maximum value. |
| Zero available copies | Accept the record and include it in the book table. Include it in category summaries; it contributes `0` to totals. |
| Whitespace-only title or author | Reject the submission and display a validation error. |
| Invalid category | Reject the submission and display a validation error. |
| Non-integer or negative copies | Reject the submission and display a validation error. |

## 8. Acceptance Criteria

The initial release will be considered acceptable when:

1. A librarian can add a valid book and see it in the books table after submission.
2. Invalid title, author, category, or copies values are rejected with clear feedback.
3. The total-books value equals the sum of available copies in the database.
4. The most-available result correctly handles both a unique maximum and ties.
5. Category summaries equal the grouped sum of available copies.
6. The application handles an empty database without errors.
7. Book records remain available after restarting the application.
