"""Описывает validators для приложения reviews."""
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверяет если год ещё не наступил."""
    if value > timezone.now().year:
        raise ValidationError(f"{value} год ещё не наступил")
    return value
