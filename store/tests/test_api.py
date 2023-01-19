from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BooksSerializer


# Тестируем API.
class BooksApiTestCase(APITestCase):
    def test_get(self):
        # Создаем 2 тестовых экземпляра книг.
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=55)
        url = reverse('book-list')
        # self.client предоставляется APITestCase, по сути является имитацией клиента, в том числе браузера.
        response = self.client.get(url)

        # many=True означает, что сериализовать нужно все объекты.
        serializer_data = BooksSerializer([book_1, book_2], many=True).data

        # Перед тем как сравнивать сами данные мы должны убедиться, что код возврата
        # http сервиса будет 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)





