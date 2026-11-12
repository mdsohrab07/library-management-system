import sqlite3

import streamlit as st

from database import (
    add_book,
    get_all_books,
    get_category_summary,
    get_most_available_book,
    get_total_books,
    init_db,
)


PAGE_TITLE = "ABC Engineering College – Library Management System"
BOOK_CATEGORIES = [
    "Programming",
    "Artificial Intelligence",
    "Data Science",
    "Mathematics",
    "Electronics",
    "Management",
]


def add_book_page() -> None:
    """Render the form for adding a book."""
    st.header("Add Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")
        category = st.selectbox("Category", BOOK_CATEGORIES)
        copies = st.number_input(
            "Available Copies",
            min_value=0,
            value=0,
            step=1,
            format="%d",
        )
        submitted = st.form_submit_button("Save Book")

    if submitted:
        if not title.strip() or not author.strip():
            st.error("Book title and author name cannot be blank.")
            return

        try:
            add_book(title.strip(), author.strip(), category, int(copies))
        except sqlite3.IntegrityError:
            st.error(
                "The book could not be saved because the data is invalid."
            )
            return
        except sqlite3.Error:
            st.error("The book could not be saved. Please try again.")
            return
        st.success("Book saved successfully.")


def view_books_page() -> None:
    """Render all books in a table."""
    st.header("View Books")
    books = get_all_books()
    if not books:
        st.info("No books have been added yet.")
        return

    st.dataframe(
        [
            {
                "Book ID": book_id,
                "Title": title,
                "Author": author,
                "Category": category,
                "Available Copies": copies,
            }
            for book_id, title, author, category, copies in books
        ],
        use_container_width=True,
        hide_index=True,
    )


def total_books_page() -> None:
    """Render the total number of available book copies."""
    st.header("Total Books")
    st.metric("Total Available Copies", get_total_books())


def most_available_book_page() -> None:
    """Render every book tied for the highest stock."""
    st.header("Most Available Book")
    books = get_most_available_book()
    if not books:
        st.info("No books have been added yet.")
        return

    if len(books) > 1:
        st.info("Several books are tied for the highest available stock.")

    st.dataframe(
        [
            {
                "Title": title,
                "Author": author,
                "Category": category,
                "Available Copies": copies,
            }
            for _, title, author, category, copies in books
        ],
        use_container_width=True,
        hide_index=True,
    )


def category_summary_page() -> None:
    """Render category totals as a table and bar chart."""
    st.header("Category Summary")
    summary = get_category_summary()
    if not summary:
        st.info("No category data is available yet.")
        return

    summary_data = [
        {"Category": category, "Total Copies": total_copies}
        for category, total_copies in summary
    ]
    st.dataframe(summary_data, use_container_width=True, hide_index=True)
    st.bar_chart(
        data=summary_data,
        x="Category",
        y="Total Copies",
        x_label="Category",
        y_label="Total Copies",
    )


def main() -> None:
    """Initialize the database and render the selected application page."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📚")
    try:
        init_db()
    except sqlite3.Error:
        st.error("The library database could not be initialized.")
        st.stop()

    st.title(PAGE_TITLE)
    st.sidebar.caption("ABC Engineering College")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Add Book",
            "View Books",
            "Total Books",
            "Most Available Book",
            "Category Summary",
        ],
    )

    pages = {
        "Add Book": add_book_page,
        "View Books": view_books_page,
        "Total Books": total_books_page,
        "Most Available Book": most_available_book_page,
        "Category Summary": category_summary_page,
    }
    pages[page]()


if __name__ == "__main__":
    main()
