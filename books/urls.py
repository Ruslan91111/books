from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet


# Создаем экземпляр класса SimpleRouter.
router = SimpleRouter()
# Добавим в наш router view.
router.register(r'book', BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
]

# Добавляем urls нашего router.
urlpatterns += router.urls