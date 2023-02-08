from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer


# Тестируем работу сериализатора.
# В var data собираем результат работы сериализатора, т.е. сериализацию двух тестовых объектов.
# В var expected_data, то что ожидаем увидеть от работы сериализатора.
# Сравниваем обе переменных
class BookSerializerTestCase(TestCase):
    """Test work of serializer"""
    def test_ok(self):
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 2')
        data = BooksSerializer([book_1, book_2], many=True)
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1'
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2'
            },
        ]
        self.assertEqual(expected_data, data.data)

