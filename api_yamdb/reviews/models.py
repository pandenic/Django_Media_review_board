from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Описание дополнительных полей модели User."""

    ROLES = (
        ("user", "user"),
        ("admin", "admin"),
        ("moderator", "moderator"),
    )

    bio = models.TextField(
        verbose_name="Биография",
        help_text="Укажите биографию пользователей",
        blank=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        help_text="Укажите роль пользователя",
        max_length=9,
        default="user",
        choices=ROLES,
    )
