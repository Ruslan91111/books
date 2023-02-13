from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)

    # DecimalField типа float, только фиксируем количество цифр.
    # В данном примере 5 цифр до запятой, 2 после.
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    # Связь многие ко многим, будет осуществляться через созданный нами класс UserBookRelation, указанный в through,
    # но при этом и без класса она могла бы осуществляться по ManyToMany.
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     related_name='books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    # Переопределение магического метода - строкового представления экземпляра класса.
    def __str__(self):
        return f'Id {self.id}: {self.name}'


# Модель хранения отношений между пользователями и книгами.
class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.book.name}, {self.rate}'

    # Функция, вызывающаяся каждый раз при сохранении модели - ее создании и обновлении.
    def save(self, *args, **kwargs):
        from store.logic_rating import set_rating

        # True если экземпляр создается и нет у него РК, False - если уже был ранее создан
        creating = not self.pk
        old_rating = self.rate

        super().save(*args, **kwargs)

        new_rating = self.rate
        if old_rating != new_rating or creating:
            set_rating(self.book)




