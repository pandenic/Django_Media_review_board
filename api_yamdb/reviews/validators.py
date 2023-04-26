"""Описывает validators для приложения reviews."""
from django.core.exceptions import ValidationError
from django.utils import timezone

from api.errors import ErrorMessage


def validate_year(value):
    """Проверяет если год ещё не наступил."""
    if value > timezone.now().year:
        raise ValidationError(f"{value} {ErrorMessage.INVALID_YEAR_ERROR}")
    return value
