"""Содержит настройки конфигурации приложения reviews."""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Конфигурирует приложение reviews."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
