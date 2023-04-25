"""Содержит настройки конфигурации приложения api."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Конфигурирует приложение api."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
