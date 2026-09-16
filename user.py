## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    LIBRARY_FILE,
    display_books,
    find_book,
    load_library,
    save_library,
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    needle = category.strip().casefold() if isinstance(category, str) else ""
    if not needle or not isinstance(books, dict):
        return []

    matching_ids = []
    for book_id, book in books.items():
        book_category = str(book.get("category", "")).strip()
        if book_category.casefold() == needle:
            matching_ids.append(book_id)
    return matching_ids

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    needle = search_text.strip().casefold() if isinstance(search_text, str) else ""
    if not needle or not isinstance(books, dict):
        return []

    matching_ids = []
    for book_id, book in books.items():
        title = str(book.get("title", ""))
        if needle in title.casefold():
            matching_ids.append(book_id)
    return matching_ids
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not isinstance(borrower, str) or not borrower.strip():
        return "EMPTY_NAME"

    if not books[book_id].get("available"):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower,
    })
    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not isinstance(borrower, str) or not borrower.strip():
        return "EMPTY_NAME"

    loan_index = None
    for index, loan in enumerate(loans):
        if loan.get("book_id") == book_id:
            loan_index = index
            break

    if loan_index is None or books[book_id].get("available"):
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    loans.pop(loan_index)
    return "OK"

    



def _print_matching_books(books, book_ids):
    if not book_ids:
        print("No books found.")
        return

    matching_books = {
        book_id: books[book_id]
        for book_id in book_ids
        if book_id in books
    }
    display_books(matching_books)


## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library(LIBRARY_FILE)
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY USER SYSTEM")
    print("============================================================")

    while True:
        print()
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            search_text = input("Enter title: ")
            matching_ids = search_by_title(books, search_text)
            _print_matching_books(books, matching_ids)
        elif choice == "2":
            category = input("Enter category: ")
            matching_ids = books_in_category(books, category)
            _print_matching_books(books, matching_ids)
        elif choice == "3":
            search_text = input("Enter book ID, title, or author: ")
            borrower = input("Enter borrower name: ")
            result = borrow_book(books, loans, search_text, borrower)
            print(result)
        elif choice == "4":
            book_title = input("Enter book ID, title, or author: ")
            borrower = input("Enter borrower name: ")
            result = return_book(books, loans, book_title, borrower)
            print(result)
        elif choice == "5":
            data["books"] = books
            data["loans"] = loans
            save_library(data, LIBRARY_FILE)
            print("Goodbye.")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
