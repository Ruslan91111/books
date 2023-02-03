from rest_framework.serializers import ModelSerializer

from .models import Book


# Сериализатор — переводит структуры данных в последовательность байтов.
class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

