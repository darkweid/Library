import json


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = 'В наличии'):
        """
        Initialize a new book.

        :param book_id: Unique identifier for the book.
        :param title: The title of the book.
        :param author: The author of the book.
        :param year: The year the book was published.
        :param status: The availability status of the book. Default is 'В наличии'.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self) -> str:
        """
        String representation of the book.

        :return: A string representing the book's ID, title, author, year, and status.
        """
        return f'{self.book_id}: {self.title} by {self.author} ({self.year}) - {self.status}'


class Library:
    def __init__(self, data_file: str = 'data.json'):
        """
        Initialize a new library and load books from the specified file.

        :param data_file: Path to the JSON file where book data is stored.
        """
        self.data_file = data_file
        self.books: list[Book] = []
        self.load_from_file()

    def load_from_file(self) -> None:
        """
        Load books from the JSON file into the library.

        This method is called during initialization to populate the library's books list.
        If the file is not found, the library will be empty.
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book(**book) for book in data]
        except FileNotFoundError:
            self.books = []

    def save_to_file(self) -> None:
        """
        Save the current list of books to the JSON file.

        This method saves the books' data to the file in a readable JSON format.
        """
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Add a new book to the library.

        :param title: The title of the new book.
        :param author: The author of the new book.
        :param year: The year the new book was published.
        """
        book_id = max((book.book_id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_to_file()

    def remove_book(self, book_id: int) -> bool:
        """
        Remove a book from the library by its ID.

        :param book_id: The ID of the book to be removed.
        :return: True if the book was removed, False if the book with the given ID does not exist.
        """
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_to_file()
            return True
        return False

    def search_books(self, query: str, field: str) -> list[Book]:
        """
        Search for books by a specific field (title, author, or year).

        :param query: The search query to look for in the books' field.
        :param field: The field to search in (title, author, or year).
        :return: A list of books that match the search query.
        """
        return [book for book in self.books if query.lower() in str(getattr(book, field, '')).lower()]

    def display_books(self) -> None:
        """
        Display all books in the library.

        If the library is empty, a message is displayed stating that no books are available.
        """
        if not self.books:
            print('Библиотека пуста.')
        else:
            for book in self.books:
                print(book)

    def book_exists(self, book_id: int) -> bool:
        """
        Check if a book exists in the library by its ID.

        :param book_id: The ID of the book to check.
        :return: True if the book exists, False otherwise.
        """
        return any(b.book_id == book_id for b in self.books)

    def get_book_by_id(self, book_id: int) -> Book | None:
        """
        Get a book by its ID.

        :param book_id: The ID of the book to retrieve.
        :return: The book if found, None if no book with the given ID exists.
        """
        return next((b for b in self.books if b.book_id == book_id), None)

    def change_status(self, book_id: int, status: str) -> bool:
        """
        Change the status of a book by its ID.

        :param book_id: The ID of the book whose status will be changed.
        :param status: The new status for the book.
        :return: True if the status was updated, False if the book with the given ID does not exist.
        """
        book = self.get_book_by_id(book_id)
        if book:
            book.status = status
            self.save_to_file()
            return True
        return False
