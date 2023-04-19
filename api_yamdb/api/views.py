from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title
from api.serializers import TitleViewSerializer
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    """GET-запрос вернет список всех произведений
    Доступна фильтрация по полям."""

    queryset = Title.objects.all()
    serializer_class = TitleViewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
