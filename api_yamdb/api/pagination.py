"""Модуль содержит определения pagination классов."""
from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Описывае правила pagination для класса User."""

    page_size = 20
