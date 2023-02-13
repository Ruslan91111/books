from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


# Тестируем работу сериализатора.
# В переменной data собираем результат работы сериализатора, т.е. сериализацию двух тестовых объектов.
# В переменной expected_data, то что ожидаем увидеть от работы сериализатора.
# Сравниваем обе переменных

class BookSerializerTestCase(TestCase):
    """Test work of serializer"""
    def test_ok(self):
        # Три тестовых пользователя.
        user1 = User.objects.create(username='user1',
                                    first_name='Ivan', last_name='Drago')
        user2 = User.objects.create(username='user2',
                                    first_name='Apollo', last_name='Creed')
        user3 = User.objects.create(username='user3',
                                    first_name='Vin', last_name='Diesel')

        # Две тестовых книги.
        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 2')

        # Шесть тестовых отношений.
        UserBookRelation.objects.create(user=user1, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True,
                                        rate=5)
        # Переменной присваиваем созданный объект отношений,
        # атрибуту rate присваиваем значение 4.
        user_book_3 = UserBookRelation.objects.create(user=user3, book=book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=user1, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        # queryset для теста. Переменной books присваиваем queryset из лайкнутых книг,
        # при этом каждой книге аннотируем поле annotated_likes, которому присваиваем
        # количество лайков, которое считаем в случае, когда имеется связь между
        # книгой и пользователем, тогда для подсчета используется единица.
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')

        # Здесь вручную передаем сериализатору две книги.
        # При этом во viewset передается queryset.
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                # 'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Drago'
                    },
                    {
                        'first_name': 'Apollo',
                        'last_name': 'Creed'
                    },
                    {
                        'first_name': 'Vin',
                        'last_name': 'Diesel'
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                # 'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Drago'
                    },
                    {
                        'first_name': 'Apollo',
                        'last_name': 'Creed'
                    },
                    {
                        'first_name': 'Vin',
                        'last_name': 'Diesel'
                    }
                ]
            },
        ]

        self.assertEqual(expected_data, data)

