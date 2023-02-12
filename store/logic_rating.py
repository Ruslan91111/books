from django.db.models import Avg

from store.models import UserBookRelation


# Функция по установке рейтинга.
def set_rating(book):
    rating = UserBookRelation.objects.filter(book=book).aggregate(
        rating=Avg('rate')).get('rating')
    # Сохранить полученный результат - рейтинг.
    book.rating = rating
    book.save()


