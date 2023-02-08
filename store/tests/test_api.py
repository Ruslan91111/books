import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BooksSerializer


# Тестируем API - запросы.
class BooksApiTestCase(APITestCase):
    """Test work of API"""
    # Функция setUp будет запускаться каждый раз перед каждым нашим тестом.
    def setUp(self):
        # Создаем тестового пользователя, для решения вопроса с авторизацией при проверки POST запроса.
        self.user = User.objects.create(username='test_username')
        # Создаем 3 тестовых экземпляра книг в тестовой БД.
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55, author_name='Author 2')

    # Тестируем предоставления(GET) списка всех книг.
    def test_get(self):
        # DRF reverse создает нужный нам url. Для получения списка при помощи ViewSet 'book-list',
        # также можно 'book-detail'.
        url = reverse('book-list')
        # self.client предоставляется APITestCase, по сути является имитацией клиента, в том числе браузера.
        response = self.client.get(url)
        # many=True означает, что сериализовать нужно все объекты. Переменной присвоить данные после сериализации.
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        # Перед тем как сравнивать сами данные мы должны убедиться, что код возврата
        # http сервиса будет 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # Тестируем фильтр.
    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BooksSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # Тестируем поиск.
    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # Тестируем создание экземпляров.
    def test_create(self):
        # Количество книг в тестовой БД до создания книги.
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        # Создаем тестовую книгу.
        data = {
            "name": "Crime and Punishment",
            "price": 650.00,
            "author_name": "Fyodor Dostoevsky"
        }
        # Конвертируем в JSON формат
        json_data = json.dumps(data)
        # Логиним тестового пользователя.
        self.client.force_login(self.user)
        # Формируем ответ при обращении (POST) тестового пользователя к серверу, при
        # этом указываем передаваемые данные в формате json и описание типа данных.
        response = self.client.post(url, data=json_data, content_type='application/json')
        # Сравниваем ожидаемый статус соединения и получаемый статус при обращении клиента.
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # Проверяем количество книг в тестовой БД после создания книги.
        self.assertEqual(4, Book.objects.all().count())

    # Тестируем обновление экземпляра.
    def test_update(self):
        # url для изменения экземпляра с указанием id.
        url = reverse('book-detail', args=(self.book_1.id,))
        # Данные существующего в тестовой БД экземпляра с изменением цены.
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        # Конвертируем в JSON формат
        json_data = json.dumps(data)
        # Логиним тестового пользователя.
        self.client.force_login(self.user)
        # Формируем ответ при обращении (PUT) тестового пользователя к серверу, при
        # этом указываем передаваемые данные в формате json и описание типа данных.
        response = self.client.put(url, data=json_data, content_type='application/json')
        # Сравниваем ожидаемый статус соединения и получаемый статус при обращении клиента.
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Пересоздать(перезалить) экземпляр Book, поскольку наши изменения update сохранились в БД.
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        # Либо вариант попроще.
        self.book_1.refresh_from_db()

        # Проверяем, что поле реально изменилось.
        self.assertEqual(575, self.book_1.price)

    # Тестируем удаление экземпляра.
    def test_delete(self):
        # url для удаления экземпляра с указанием id.
        url = reverse('book-detail', args=(self.book_1.id,))
        # id существующего в тестовой БД экземпляра.
        data = {
            "id": self.book_1.id,
            }
        # Конвертируем в JSON формат
        json_data = json.dumps(data)
        # Логиним тестового пользователя.
        self.client.force_login(self.user)
        # Формируем ответ при обращении (delete) тестового пользователя к серверу, при
        response = self.client.delete(url, data=json_data, content_type='application/json')
        # Сравниваем ожидаемый статус соединения и получаемый статус при обращении клиента.
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Пробуем получить удаленный экземпляр книги.
        # Присваиваем переменной 'try_get_book' текст ошибки о том, что экземпляр не найден.
        try_get_book = ''
        try:
            Book.objects.get(id=self.book_1.id)
        except Exception as e:
            try_get_book = str(e)

        # Ожидаемое сообщение об ошибке.
        expecting_answer = 'Book matching query does not exist.'
        # Сравниваем ожидаемое сообщение об ошибке и сообщение, получаемое при попытке получить из БД.
        self.assertEqual(expecting_answer, try_get_book)

    # Тестируем предоставление одного экземпляра.
    def test_get_one_book(self):
        # url экземпляра с указанием id.
        url = reverse('book-detail', args=(self.book_1.id,))

        # Логиним тестового пользователя.
        self.client.force_login(self.user)
        # Формируем ответ при обращении (GET) тестового пользователя к серверу.
        response = self.client.get(url, content_type='application/json')
        # Сравниваем ожидаемый статус соединения и получаемый статус при обращении клиента.
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Ожидаемые данные.
        expecting_data = {
            "id": self.book_1.id,
            "name": self.book_1.name,
            "price": 25,
            "author_name": self.book_1.author_name
        }

        # Пропускаем через сериалайзер.
        expecting_data = BooksSerializer(expecting_data).data
        self.assertEqual(expecting_data, response.data)








