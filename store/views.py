import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Настраиваем filter, search, ordering.
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter]
    # Указываем поле, по которому хотим отфильтровать.
    filterset_fields = ['price']
    # Поля для поиска. Поиск использовать, для поиска по двум и более полям, иначе это просто фильтр.
    search_fields = ['name', 'author_name']



