from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)

    # DecimalField типа float, только фиксируем количество цифр.
    # В данном примере 5 цифр до запятой, 2 после.
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)

    # Переопределение магического метода - строкового представления экземпляра класса.
    def __str__(self):
        return f'Id {self.id}: {self.name}'


