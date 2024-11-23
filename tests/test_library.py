import pytest
import os
from library import Library


@pytest.fixture
def library():
    # Создаём временную библиотеку с временным файлом
    lib = Library(data_file='test_data.json')
    yield lib
    # После завершения тестов удалим файл
    if os.path.exists('test_data.json'):
        os.remove('test_data.json')


def test_add_book(library):
    """Test adding a book to the library."""
    initial_count = len(library.books)
    library.add_book('New Book', 'Author Name', 2021)
    assert len(library.books) == initial_count + 1
    assert library.books[-1].title == 'New Book'
    assert library.books[-1].author == 'Author Name'
    assert library.books[-1].year == 2021

def test_add_book_invalid_data(library):
    """Test adding a book with invalid data."""
    # Try adding a book with invalid data
    with pytest.raises(ValueError):
        library.add_book('', 'Author', 2021)  # Title should not be empty

    with pytest.raises(ValueError):
        library.add_book('Valid Title', 'Author', -1)  # Year should be a positive integer



def test_remove_book(library):
    """Test removing a book from the library."""
    library.add_book('Book to Remove', 'Author', 2020)
    book_id_to_remove = library.books[-1].book_id
    initial_count = len(library.books)
    assert library.remove_book(book_id_to_remove) is True
    assert len(library.books) == initial_count - 1
    assert library.remove_book(999) is False  # Non-existing book ID


def test_search_books(library):
    """Test searching books by title, author, and year."""
    library.add_book('Test Book 1', 'Test Author', 2020)
    library.add_book('Test Book 2', 'Another Author', 2021)

    # Search by title
    results = library.search_books('Test Book 1', 'title')
    assert len(results) == 1
    assert results[0].title == 'Test Book 1'

    # Search by author
    results = library.search_books('Another Author', 'author')
    assert len(results) == 1
    assert results[0].author == 'Another Author'

    # Search by year
    results = library.search_books('2020', 'year')
    assert len(results) == 1
    assert results[0].year == 2020

def test_search_books_no_results(library):
    """Test searching books when no results are found."""
    library.add_book('Test Book', 'Test Author', 2020)
    results = library.search_books('Nonexistent Author', 'author')
    assert len(results) == 0

    results = library.search_books('9999', 'year')
    assert len(results) == 0



def test_change_status(library):
    """Test changing the status of a book."""
    library.add_book('Test Book', 'Test Author', 2020)
    book_id = library.books[-1].book_id

    # Change status to 'Выдана'
    assert library.change_status(book_id, 'Выдана') is True
    assert library.books[-1].status == 'Выдана'

    # Try changing status to an invalid book ID
    assert library.change_status(999, 'В наличии') is False


def test_book_exists(library):
    """Test checking if a book exists in the library by its ID."""
    library.add_book('Test Book', 'Test Author', 2020)
    book_id = library.books[-1].book_id
    assert library.book_exists(book_id) is True
    assert library.book_exists(999) is False


def test_display_books(library):
    """Test displaying all books."""
    library.add_book('Test Book', 'Test Author', 2020)
    library.add_book('Another Book', 'Another Author', 2021)
    # We will redirect stdout to capture the print statements
    from io import StringIO
    import sys
    captured_output = StringIO()
    sys.stdout = captured_output

    library.display_books()
    sys.stdout = sys.__stdout__  # Reset redirect

    # Check if the display output contains the books' details
    assert 'Test Book' in captured_output.getvalue()
    assert 'Another Book' in captured_output.getvalue()

def test_display_books_empty(library):
    """Test displaying books when the library is empty."""
    # Redirect stdout
    from io import StringIO
    import sys
    captured_output = StringIO()
    sys.stdout = captured_output

    library.display_books()
    sys.stdout = sys.__stdout__  # Reset redirect

    # Check if the display output contains the message for an empty library
    assert 'Библиотека пуста.' in captured_output.getvalue()

