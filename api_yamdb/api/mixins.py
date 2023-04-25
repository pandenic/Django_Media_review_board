"""Модуль содержит viewset mixins для приложения api."""
from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Определяет mixin для методов list, creat, destroy."""

    pass
