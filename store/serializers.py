from rest_framework.serializers import ModelSerializer

from .models import Book, UserBookRelation


# Сериализатор — переводит структуры данных в последовательность байтов.
class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# Сериализатор для работы пользователя с книгами(лайки, оценки)
class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')


