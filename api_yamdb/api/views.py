from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title
from .serializers import TitleSerializer
from .filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    """GET-запрос вернет список всех произведений
    Доступна фильтрация по полям."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    # TODO: permission_classes
