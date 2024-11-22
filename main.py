from library import Library


def main():
    library = Library()

    while True:
        print('\nМеню:')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книгу')
        print('4. Показать все книги')
        print('5. Изменить статус книги')
        print('0. Завершить работу')
        choice = input('Выберите действие: ')

        if choice == '1':
            title = input('Введите название книги: ')
            author = input('Введите автора книги: ')
            year = int(input('Введите год издания книги: '))
            library.add_book(title, author, year)
            print('Книга добавлена.')
        elif choice == '2':
            book_id = int(input('Введите ID книги для удаления: '))
            if library.remove_book(book_id):
                print('Книга удалена.')
            else:
                print('Книга с таким ID не найдена.')
        elif choice == '3':
            field = input('Введите поле для поиска (title, author, year): ')
            query = input('Введите значение для поиска: ')
            results = library.search_books(query, field)
            if results:
                for book in results:
                    print(book)
            else:
                print('Книги не найдены.')
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input('Введите ID книги: '))
            status = input('Введите новый статус (В наличии/Выдана): ')
            if library.change_status(book_id, status):
                print('Статус обновлен.')
            else:
                print('Ошибка обновления статуса.')
        elif choice == '0':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()
