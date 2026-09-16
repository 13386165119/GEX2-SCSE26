##Import the necessary module
import json


LIBRARY_FILE = "library.json"


def _normalize_text(value):
    if not isinstance(value, str):
        return ""
    return value.strip()


## This function should load the library data from a JSON file and return it as a suitable Python data structure.
def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)



## This function should save the library data to a JSON file.
## This function does not need to return anything, but it should ensure that the data is saved correctly to the specified file.
def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    



## This function should find a book by its title, author, or ID.
## If the book is found, it should return the book ID.
## If the book is not found, it should return None.
def find_book(books, search_text):
    needle = _normalize_text(search_text).casefold()
    if not needle or not isinstance(books, dict):
        return None

    for book_id, book in books.items():
        if _normalize_text(str(book_id)).casefold() == needle:
            return book_id

    for book_id, book in books.items():
        title = _normalize_text(book.get("title", ""))
        author = _normalize_text(book.get("author", ""))
        if title.casefold() == needle or author.casefold() == needle:
            return book_id

    for book_id, book in books.items():
        title = _normalize_text(book.get("title", ""))
        author = _normalize_text(book.get("author", ""))
        if needle in title.casefold() or needle in author.casefold():
            return book_id

    return None



## This function should display the list of books in a user-friendly format.
## It should show the book ID, title, category, and availability status (available or on loan).
## If the book is available, it should display "AVAILABLE", and if it is on loan, it should display "ON LOAN".
## The function should not return anything, but it should print the information to the console.
## The heading for this display should be "BOOK CATALOGUE".
def display_books(books):
    print("BOOK CATALOGUE")
    print("------------------------------------------------------------")
    if not isinstance(books, dict):
        return

    for book_id, book in books.items():
        title = book.get("title", "")
        category = book.get("category", "")
        availability = "AVAILABLE" if book.get("available") else "ON LOAN"
        print(f"{book_id} | {title} | {category} | {availability}")


## This function should display the list of current loans in a user-friendly format.
## It should show the book ID, title, and the name of the borrower.
## The heading for this display should be "CURRENT LOANS".
## The function should not return anything, but it should print the information to the console.
def display_loans(loans, books):
    print("CURRENT LOANS")
    print("------------------------------------------------------------")
    if not isinstance(loans, list):
        return

    books = books if isinstance(books, dict) else {}
    for loan in loans:
        book_id = loan.get("book_id", "")
        borrower = loan.get("borrower", "")
        title = books.get(book_id, {}).get("title", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")


## This function should calculate and return the library statistics
## The statsitics should include the total number of books, the number of available books, and the number of borrowed books.
## The function should return these three values in the order: total, available, borrowed. Use a suitable data structure to return these values, such as a tuple or a dictionary.

def library_statistics(books):
    if not isinstance(books, dict):
        return (0, 0, 0)

    total = len(books)
    available = 0
    for book in books.values():
        if book.get("available"):
            available += 1
    borrowed = total - available
    return (total, available, borrowed)


## This function should display the library statistics in a user-friendly format.
## It should first load the library data from a JSON file, 
## Then calculate the statistics, and finally print the information to the console.
## The heading for this display should be "LIBRARY STATISTICS".
## It should print the total number of books, the number of available books, and the number of borrowed books.
## The function should not return anything, but it should print the information to the console.
def main():
    data = load_library(LIBRARY_FILE)
    library = data.get("library", {})
    categories = data.get("categories", [])
    books = data.get("books", {})
    loans = data.get("loans", [])
    total, available, borrowed = library_statistics(books)

    print("LIBRARY ADMINISTRATION")
    print("============================================================")
    print(f"Library: {library.get('name', '')}")
    print(f"Branch: {library.get('branch', '')}")
    print(f"Year: {library.get('year', '')}")
    print(f"Categories: {', '.join(str(category) for category in categories)}")
    print()
    display_books(books)
    print()
    display_loans(loans, books)
    print()
    print("STATISTICS")
    print("------------------------------------------------------------")
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()
