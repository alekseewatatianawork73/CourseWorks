import json

with open('books.json', 'r+', encoding='UTF-8') as file:
    books = json.load(file)

# общая функция поиска для 1 - 4 запросов
def search(input_data, condition):
    """cmp = lambda a, b: a >= float(b) if condition == 'Рейтинг Litres' else lambda a, b: a == b
    return set(name for name, values in books.items() if cmp(values[condition].lower(), input_data.lower()))"""
    if condition == 'Рейтинг Litres':
        return set(name for name, values in books.items() if values[condition] >= float(input_data))
    return set(name for name, values in books.items() if values[condition].lower() == input_data.lower())


# общая функция поиска для 5 - 7 запросов
def span(start, finish, condition):
    return set(name for name in books.keys() if start <= books[name][condition] <= finish)


# вывод информации о книге (8 запрос)
def book_info(input_data):
    book = books.get(input_data.capitalize())
    if book:
        return (f"{input_data.capitalize()}:\nАвтор: {book['Автор']}\n"
                f"Жанр: {book['Жанр']}\n"
                f"Страна оригинала: {book['Страна оригинала']}\n"
                f"Год написания: {book['Год написания']}\n"
                f"Примерный объём книги: {book['Объём книги (в страницах)']} страниц\n"
                f"Рейтинг Litres: {book['Рейтинг Litres']}\n"
                f"Средняя стоимость: {book['Средняя стоимость (в рублях)']} рублей\n")
    return "Книга с указанным названием не найдена."


# функция для запросов 9 и 10
def roster(data=None):
    return sorted(set(books[book]['Автор'] if data == 'Автор' else book for book in books.keys()), reverse=True)
