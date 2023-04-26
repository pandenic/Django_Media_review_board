"""Модуль содержит определения permissions для приложения api."""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Ограничмвает использование 'опасных' запросов.

    Для всех кроме админа.
    """

    def has_permission(self, request, view):
        """Проверяет запрос на соответствие ограничениям."""
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.role == request.user.ROLE_ADMIN
        )


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Ограничмвает использование 'опасных' запросов.

    Для всех кроме модератора и админа.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет доступ к объекту на соответствие ограничениям."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.role == request.user.ROLE_ADMIN
        )


class IsAdminOnly(permissions.BasePermission):
    """Ограничмвает использование любых запросов.

    Для всех кроме модератора и админа.
    """

    def has_permission(self, request, view):
        """Проверяет запрос на соответствие ограничениям."""
        return (
            request.user.is_superuser
            or request.user.role == request.user.ROLE_ADMIN
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Ограничмвает использование 'опасных' запросов.

    Для всех кроме любого аутентифицированного пользователя.
    """

    def has_permission(self, request, view):
        """Проверяет запрос на соответствие ограничениям."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == request.user.ROLE_ADMIN
        return False
