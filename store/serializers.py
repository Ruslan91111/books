from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Book, UserBookRelation


# Сериализатор — переводит структуры данных в последовательность байтов.

class BooksSerializer(ModelSerializer):
    # var для подсчета вручную.
    likes_count = serializers.SerializerMethodField()
    # Подсчет через Annotate
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count',
                  'annotated_likes', 'rating')

    # Посчитать количество лайков вручную.
    # self - сам сериализатор, instance - то, что мы сериализуем.
    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


# Сериализатор для работы пользователя с книгами(лайки, оценки)
class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')


