from library import Library
from collections import namedtuple

SearchField = namedtuple('SearchField', ['option', 'description', 'query_text', 'field'])
search_fields = [
    SearchField('1', 'По названию', 'название', 'title'),
    SearchField('2', 'По автору', 'автора', 'author'),
    SearchField('3', 'По году издания', 'год издания', 'year')
]


def display_menu() -> str:
    """
    Displays the menu of available actions for the user.

    Returns:
        str: The user's choice from the menu.
    """
    print('\nМеню:')
    print('1. Добавить книгу')
    print('2. Удалить книгу')
    print('3. Найти книгу')
    print('4. Показать все книги')
    print('5. Изменить статус книги')
    print('0. Завершить работу')
    return input('Выберите действие: ')


def add_book(library: Library) -> None:
    """
    Adds a new book to the library.

    Prompts the user for book title, author, and publication year,
    and adds the book to the library with a unique ID and a default status.
    """
    title = input('Введите название книги: ')
    author = input('Введите автора книги: ')
    try:
        year = int(input('Введите год издания книги: '))
        library.add_book(title, author, year)
        print('Книга добавлена.')
    except ValueError:
        print('Год издания должен быть числом.')


def delete_book(library: Library) -> None:
    """
    Deletes a book from the library by its ID.

    Displays all books and prompts the user for the book's ID to remove.
    If the book with the given ID is not found, an error message is displayed.
    """
    library.display_books()
    try:
        book_id = int(input('Введите ID книги для удаления: '))
        if library.remove_book(book_id):
            print('Книга удалена.')
        else:
            print('Книга с таким ID не найдена.')
    except ValueError:
        print('ID должен быть числом.')


def search_book(library: Library) -> None:
    """
    Searches for books in the library based on a selected parameter (title, author, or year).

    Displays search options and prompts the user for input to filter books.
    Results are displayed if any matches are found.
    """
    print('\nПараметры поиска:')
    for field in search_fields:
        print(f'{field.option}. {field.description}')
    choice = input('Выберите параметр поиска: ')
    field = next((f for f in search_fields if f.option == choice), None)
    if field:
        query = input(f'Введите {field.query_text} книги: ')
        results = library.search_books(query, field.field)
        if results:
            for book in results:
                print(book)
        else:
            print('Книги не найдены.')
    else:
        print('Некорректный выбор параметра поиска.')


def update_status(library: Library) -> None:
    """
    Updates the status of a book (available or issued) based on its ID.

    Prompts the user for a book ID and a new status. If the book exists,
    the status is updated. If the book is not found, an error message is displayed.
    """
    try:
        book_id = int(input('Введите ID книги: '))
        if not library.book_exists(book_id):
            print(f'Книга с ID {book_id} не найдена.')
            return
        status = input('Выберите новый статус (1 - В наличии, 2 - Выдана): ')
        if status == '1':
            library.change_status(book_id, 'В наличии')
            print('Статус обновлён.')
        elif status == '2':
            library.change_status(book_id, 'Выдана')
            print('Статус обновлён.')
        else:
            print('Некорректный статус.')
    except ValueError:
        print('ID должен быть числом.')


def display_books(library: Library) -> None:
    """
    Displays all books in the library.

    Prints the details of each book currently stored in the library.
    """
    library.display_books()


def main() -> None:
    """
    Main function that runs the library management system.

    Displays a welcome message and then continuously prompts the user
    for an action until they choose to exit the program.
    """
    print('Добро пожаловать в систему управления библиотекой!')
    print('Здесь вы можете добавлять, удалять, искать и отображать книги.')
    print('Используйте цифры в меню, чтобы выбрать необходимое действие.')

    library = Library()

    actions = {
        '1': add_book,
        '2': delete_book,
        '3': search_book,
        '4': display_books,
        '5': update_status,
    }

    while True:
        choice = display_menu()
        if choice == '0':
            print('Выход из программы.')
            break
        action = actions.get(choice)
        if action:
            action(library)
        else:
            print('Некорректный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()
