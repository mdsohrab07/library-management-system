# Test Cases

## Automated database tests

Run the database tests from the project directory:

```powershell
py -m pytest tests/test_database.py -q
```

The tests use `tmp_path` and monkeypatch `database.DATABASE_PATH`, so they do
not create or modify the project's `library.db`.

## Manual Streamlit UI checklist

Start the application:

```powershell
streamlit run app.py
```

Use the sidebar to select each page and confirm the following behavior.

### 1. Add Book

- [ ] The page displays Book Title, Author Name, Category, Available Copies,
      and a save button.
- [ ] The category selectbox contains Programming, Artificial Intelligence,
      Data Science, Mathematics, Electronics, and Management.
- [ ] Available Copies accepts integer values from `0` upward and does not
      allow negative values.
- [ ] Enter a valid book and submit it; a success message appears.
- [ ] The saved book appears on the View Books page.
- [ ] Submit with a blank title; an error message appears and no book is saved.
- [ ] Submit with a blank author; an error message appears and no book is saved.

### 2. View Books

- [ ] The table has Book ID, Title, Author, Category, and Available Copies
      columns.
- [ ] Saved records appear with the expected values.
- [ ] With no records, an informational empty-state message appears instead of
      an error.

### 3. Total Books

- [ ] The page displays a metric for total available copies.
- [ ] The metric equals the sum of Available Copies for all saved books.
- [ ] With no records, the metric displays `0`.

### 4. Most Available Book

- [ ] The page displays the title, author, category, and copies for the book
      with the highest stock.
- [ ] Add two books with the same highest stock and confirm both are displayed.
- [ ] With no records, an informational empty-state message appears.

### 5. Category Summary

- [ ] The page displays a category-wise table with category and total copies.
- [ ] Category totals equal the sum of copies for books in each category.
- [ ] A bar chart is displayed using the category totals.
- [ ] With no records, an informational empty-state message appears.
