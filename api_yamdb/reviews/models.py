"""Модуль содержит описание моделей для приложения review."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import validate_year


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


class Category(models.Model):
    """Модель описывает категории произведений.

    Включает поля name и slug.
    """

    name = models.CharField(
        verbose_name="Название категории",
        null=False,
        blank=False,
        unique=True,
        max_length=256,
        help_text="Укажите категорию",
    )
    slug = models.SlugField(
        verbose_name="Slug категории",
        unique=True,
        max_length=50,
        help_text="Укажите slug категории",
    )

    class Meta:
        """Определяет настройки модели Category."""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Модель описывает жанры произведений.

    Включает поля name и slug.
    """

    name = models.CharField(
        verbose_name="Название жанра",
        null=False,
        blank=False,
        unique=True,
        max_length=256,
        help_text="Укажите жанр",
    )
    slug = models.SlugField(
        verbose_name="Slug жанра",
        unique=True,
        max_length=50,
        help_text="Укажите slug жанра",
    )

    class Meta:
        """Определяет настройки модели Genre."""

        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """Модель, описывающая произведения."""

    name = models.CharField(
        verbose_name="Название",
        null=False,
        blank=False,
        unique=False,
        max_length=256,
        help_text="Добавьте название",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Добавьте описание",
    )
    year = models.IntegerField(
        verbose_name="Год выхода",
        null=False,
        blank=False,
        validators=[validate_year],
        help_text="Укажите год выхода",
    )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        help_text="Укажите категорию",
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанр",
        help_text="Укажите жанр",
    )

    class Meta:
        """Определяет настройки модели Title."""

        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        """Определяет отображение модели Title."""
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для связи ManytoMany.

    Между произведением и жанром.
    """

    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        help_text="Укажите произведение",
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        on_delete=models.CASCADE,
        help_text="Укажите жанр",
    )

    class Meta:
        """Определяет настройки модели GenreTitle."""

        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"

    def __str__(self):
        """Определяет отображение модели GenreTitle."""
        return f"{self.title}, {self.genre}"
