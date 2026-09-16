import json


def load_library(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def find_book(books, search_text):
    if search_text is None:
        return None
    key = search_text.strip().lower()
    if not key:
        return None
    for book_id, book in books.items():
        if book_id.lower() == key:
            return book_id
        if book.get("title", "").lower() == key:
            return book_id
        if book.get("author", "").lower() == key:
            return book_id
    return None


def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book.get("available") else "ON LOAN"
        print(f"{book_id} | {book.get('title')} | {book.get('category')} | {status}")


def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan.get("book_id")
        book = books.get(book_id)
        if book is None:
            continue
        print(f"{book_id} | {book.get('title')} | Borrower: {loan.get('borrower')}")


def library_statistics(books):
    total = len(books)
    available = 0
    for book in books.values():
        if book.get("available"):
            available += 1
    borrowed = total - available
    return (total, available, borrowed)


def main():
    data = load_library("library.json")
    lib = data.get("library", {})
    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {lib.get('name')}")
    print(f"Branch: {lib.get('branch')}")
    print(f"Year: {lib.get('year')}")
    print(f"Categories: {', '.join(data.get('categories', []))}")
    print()
    display_books(data.get("books", {}))
    print()
    display_loans(data.get("loans", []), data.get("books", {}))
    print()
    print("STATISTICS")
    print("-" * 60)
    total, available, borrowed = library_statistics(data.get("books", {}))
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()