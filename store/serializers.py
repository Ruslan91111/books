from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Book, UserBookRelation


# Сериализатор — переводит структуры данных в последовательность байтов.


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    # Переменная для подсчета вручную.
    # likes_count = serializers.SerializerMethodField()

    # Подсчет через Annotate
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    # source - откуда берем имя владельца книги. Book.owner -> User -> AbstractUser.username
    # пример наследования. owner.username атрибут username ищется в дереве атрибутов и находится у AbstractUser
    owner_name = serializers.CharField(source='owner.username', default='',
                                       read_only=True)
    # Чтобы вложить нашего reader внутрь словаря с книгой.
    readers = BookReaderSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'annotated_likes', 'rating', 'owner_name', 'readers')

    # Посчитать количество лайков вручную.
    # self - сам сериализатор, instance - то, что мы сериализуем.
    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


# Сериализатор для работы пользователя с книгами(лайки, оценки)
class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')


