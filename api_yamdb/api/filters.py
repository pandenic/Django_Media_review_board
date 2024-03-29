"""Модуль содержит фильтры для приложения api."""
from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Фильтрует произведения по полям."""

    genre = filters.CharFilter(field_name="genre__slug", lookup_expr="exact")
    category = filters.CharFilter(
        field_name="category__slug",
        lookup_expr="exact",
    )
    name = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        """Определяет настройки фильтра TitleFilter."""

        model = Title
        fields = "__all__"
