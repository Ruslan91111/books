from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    The request user is an owner, or is a read-only request.
    """
    # Если SAFE_METHODS пусть читает, даже если не авторизован.
    # Если метод небезопасный, то пользователь должен быть аутентифицирован и
    # владельцем объекта - книги, либо не владелец, но из персонала.
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.owner == request.user or request.user.is_staff)
        )




