from admin import (
    load_library,
    save_library,
    find_book
)


def books_in_category(books, category):
    if category is None:
        return []
    key = category.strip().lower()
    if not key:
        return []
    result = []
    for book_id, book in books.items():
        if book.get("category", "").lower() == key:
            result.append(book_id)
    return result


def search_by_title(books, search_text):
    if search_text is None:
        return []
    key = search_text.strip().lower()
    if not key:
        return []
    result = []
    for book_id, book in books.items():
        if key in book.get("title", "").lower():
            result.append(book_id)
    return result


def borrow_book(books, loans, search_text, borrower):
    if borrower is None or borrower.strip() == "":
        return "EMPTY_NAME"
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    if not books[book_id].get("available"):
        return "NOT_AVAILABLE"
    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower.strip()})
    return "OK"


def return_book(books, loans, book_title, borrower):
    if borrower is None or borrower.strip() == "":
        return "EMPTY_NAME"
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    found = None
    for loan in loans:
        if loan.get("book_id") == book_id:
            found = loan
            break
    if found is None:
        return "NOT_ON_LOAN"
    loans.remove(found)
    books[book_id]["available"] = True
    return "OK"


def main():
    data = load_library("library.json")
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY USER SYSTEM")
    print("=" * 60)

    while True:
        print()
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            text = input("Enter title or part of title: ")
            ids = search_by_title(books, text)
            if not ids:
                print("No books found.")
            else:
                for bid in ids:
                    b = books[bid]
                    print(f"{bid} | {b.get('title')} | {b.get('category')}")

        elif choice == "2":
            cat = input("Enter category: ")
            ids = books_in_category(books, cat)
            if not ids:
                print("No books found.")
            else:
                for bid in ids:
                    b = books[bid]
                    print(f"{bid} | {b.get('title')} | {b.get('category')}")

        elif choice == "3":
            text = input("Enter book ID, title or author: ")
            name = input("Enter borrower name: ")
            result = borrow_book(books, loans, text, name)
            print(result)

        elif choice == "4":
            text = input("Enter book ID, title or author: ")
            name = input("Enter borrower name: ")
            result = return_book(books, loans, text, name)
            print(result)

        elif choice == "5":
            save_library(data, "library.json")
            print("Goodbye.")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()