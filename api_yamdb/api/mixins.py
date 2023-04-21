"""Модуль содержит viewset mixins для приложения api."""
from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Определяет mixin для методов list, creat, destroy."""

    pass
