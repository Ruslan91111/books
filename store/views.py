import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Book, UserBookRelation
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Настраиваем filter, search, ordering.
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    # Указываем поле, по которому хотим отфильтровать.
    filterset_fields = ['price']
    # Поля для поиска. Поиск использовать, для поиска по двум и более полям, иначе это просто фильтр.
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    # Переопределяем метод из CreateModelMixin, для присваивания owner во время создания книги.
    def perform_create(self, serializer):
        # Данные из сериалайзера после того как они прошли валидацию.
        # Кто создает книгу, тот и владелец, пользователя берем из запроса.
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


# Создаем представление для работы пользователя с лайками и рейтингами.
class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    # Пользователь должен быть авторизован.
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    # Для работы пользователя с книгами передавать не id Relation, а id книги.
    lookup_field = 'book'






def auth(request):
    return render(request, 'oauth.html')
