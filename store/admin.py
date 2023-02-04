from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Book


# Чтобы класс появился в админке и могли создавать объекты класса через админку.
@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass


