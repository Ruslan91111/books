from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BooksSerializer


# Тестируем API - запросы.
class BooksApiTestCase(APITestCase):
    """Test work of API"""
    def test_get(self):
        # Создаем 2 тестовых экземпляра книг в тестовой БД.
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=55)

        # DRF reverse создает нужный нам url. Для получения списка при помощи ViewSet 'book-list',
        # также можно 'book-detail'.
        url = reverse('book-list')

        # self.client предоставляется APITestCase, по сути является имитацией клиента, в том числе браузера.
        response = self.client.get(url)

        # many=True означает, что сериализовать нужно оба объекта. Переменной присвоить данные после сериализации.
        serializer_data = BooksSerializer([book_1, book_2], many=True).data

        # Перед тем как сравнивать сами данные мы должны убедиться, что код возврата
        # http сервиса будет 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)





