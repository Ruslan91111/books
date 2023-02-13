import django_filters
from django.db.models import Count, Case, When, Avg
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

    # Добавление в queryset .select_related('owner') ведет к сокращению количества и времени
    # запросов SQL, применяется LEFT OUTER JOIN. select - одного, prefetch - многих.
    queryset = Book.objects.all().annotate(
        annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
    ).select_related('owner').prefetch_related('readers').order_by('id')
    # Убрать отсюда rating, чтобы можно было создать поле rating в models.Book
    # rating=Avg('userbookrelation__rate')).select_related('owner').prefetch_related('readers').order_by('id')
    #     serializer_class = BooksSerializer

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
        # Данные из сериализатора после того как они прошли валидацию.
        # Кто создает книгу, тот и владелец, пользователя берем из запроса.
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


# Создаем представление для работы пользователя с лайками и рейтингами.
class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    # Пользователь должен быть авторизован.
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer

    # Для работы пользователя с книгами передавать не  Relation.id, а id книги.
    lookup_field = 'book'

    # Метод, который или предоставляет объект отношений, или создает, если его нет.
    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        # 'book' пришел через lookup_field, а до этого пришел в url вместо book id
        return obj


def auth(request):
    return render(request, 'oauth.html')
