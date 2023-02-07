from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, auth

# Создаем экземпляр класса SimpleRouter.
router = SimpleRouter()
# Добавим в наш router view.
router.register(r'book', BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth)

]

# Добавляем urls нашего router.
urlpatterns += router.urls