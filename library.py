import json


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = 'В наличии'):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self) -> str:
        return f'{self.book_id}: {self.title} by {self.author} ({self.year}) - {self.status}'


class Library:
    def __init__(self, data_file: str = 'data.json'):
        self.data_file = data_file
        self.books: list[Book] = []
        self.load_from_file()

    def load_from_file(self) -> None:
        '''Load books from JSON file.'''
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book(**book) for book in data]
        except FileNotFoundError:
            self.books = []

    def save_to_file(self) -> None:
        '''Save books to JSON file.'''
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        '''Add a new book to the library.'''
        book_id = max((book.book_id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_to_file()

    def remove_book(self, book_id: int) -> bool:
        '''Remove a book by ID.'''
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            self.books.remove(book)
            self.save_to_file()
            return True
        return False

    def search_books(self, query: str, field: str) -> list[Book]:
        '''Search books by title, author, or year.'''
        return [book for book in self.books if query.lower() in str(getattr(book, field, '')).lower()]

    def display_books(self) -> None:
        '''Display all books.'''
        if not self.books:
            print('Библиотека пуста.')
        else:
            for book in self.books:
                print(book)

    def change_status(self, book_id: int, status: str) -> bool:
        '''Change the status of a book.'''
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book and status in ['В наличии', 'Выдана']:
            book.status = status
            self.save_to_file()
            return True
        return False
