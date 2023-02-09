from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Book, UserBookRelation


# Чтобы класс появился в админке и могли создавать объекты класса через админку.
@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass
