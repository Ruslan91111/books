import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Настраиваем фильтр джанго.
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # Указываем поле, по которому хотим отфильтровать.
    filterset_fields = ['price']



