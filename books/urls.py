from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, auth, UserBooksRelationView

# Создаем экземпляр класса SimpleRouter.
router = SimpleRouter()
# Добавим в наш router view.
router.register(r'book', BookViewSet)
# Маршрут для работы с API отношений.
router.register(r'book_relation', UserBooksRelationView)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('__debug__/', include('debug_toolbar.urls')),
]

# Добавляем urls нашего router.
urlpatterns += router.urls


