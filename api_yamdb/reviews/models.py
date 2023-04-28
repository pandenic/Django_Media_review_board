"""Модуль содержит описание моделей для приложения review."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.errors import ErrorMessage
from reviews.validators import validate_year


class User(AbstractUser):
    """Описание дополнительных полей модели User."""

    ROLE_USER = "user"
    ROLE_ADMIN = "admin"
    ROLE_MODERATOR = "moderator"

    bio = models.TextField(
        verbose_name="Биография",
        help_text="Укажите биографию пользователей",
        blank=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        help_text="Укажите роль пользователя",
        max_length=9,
        default=ROLE_USER,
        choices=(
            (ROLE_USER, ROLE_USER),
            (ROLE_ADMIN, ROLE_ADMIN),
            (ROLE_MODERATOR, ROLE_MODERATOR),
        ),
    )

    @property
    def is_admin(self):
        """Проверяет админ ли пользователь."""
        return self.role == self.ROLE_ADMIN

    @property
    def is_moderator(self):
        """Проверяет модератор ли пользователь."""
        return self.role == self.ROLE_MODERATOR

    @property
    def is_user(self):
        """Проверяет обычный ли пользователь."""
        return self.role == self.ROLE_USER

    def save(self, *args, **kwargs):
        """Переопределяет действия при сохранении записи.

        Меняет поля is_admin и is_staff в зависимости
        от поля role.
        """
        if self.is_admin or self.is_moderator:
            self.is_staff = True
        if self.is_user:
            self.is_staff = False
        super().save(*args, **kwargs)

    class Meta:
        """Определяет настройки модели User."""

        ordering = ("role", "username")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Определяет отображение модели User."""
        return self.username


class Category(models.Model):
    """Модель описывает категории произведений.

    Включает поля name и slug.
    """

    name = models.CharField(
        verbose_name="Название категории",
        null=False,
        blank=False,
        unique=True,
        max_length=255,
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

        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Определяет отображение модели Category."""
        return self.name[:15]


class Genre(models.Model):
    """Модель описывает жанры произведений.

    Включает поля name и slug.
    """

    name = models.CharField(
        verbose_name="Название жанра",
        null=False,
        blank=False,
        unique=True,
        max_length=255,
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

        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        """Определяет отображение модели Genre."""
        return self.name[:15]


class Title(models.Model):
    """Модель, описывающая произведения."""

    name = models.CharField(
        verbose_name="Название",
        null=False,
        blank=False,
        unique=False,
        max_length=255,
        help_text="Добавьте название",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Добавьте описание",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выхода",
        null=False,
        blank=False,
        validators=(validate_year,),
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


class Review(models.Model):
    """Модель отзывов на произведения."""

    text = models.CharField(
        max_length=255,
        verbose_name="Текст отзыва",
        help_text="Введите текст отзыва",
    )
    author = models.ForeignKey(
        User,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="Автор отзыва",
        blank=True,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        blank=True,
        null=True,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        help_text=f"Укажите оценку от {settings.MIN_SCORE} до {settings.MAX_SCORE}",
        validators=(
            MinValueValidator(
                settings.MIN_SCORE,
                message=f"{ErrorMessage.MIN_SCORE_ERROR}{settings.MIN_SCORE}",
            ),
            MaxValueValidator(
                settings.MAX_SCORE,
                message=f"{ErrorMessage.MAX_SCORE_ERROR}{settings.MAX_SCORE}",
            ),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации отзыва",
    )

    class Meta:
        """Определяет настройки модели Review."""

        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=("title", "author"),
                name="unique_review",
            ),
        )

    def __str__(self) -> str:
        """Определяет отображение модели Review."""
        return self.text[:15]


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    text = models.CharField(
        max_length=255,
        verbose_name="Текст комментария",
        help_text="Текст комментария к отзывам",
    )
    author = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        related_name="comments",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария",
    )

    class Meta:
        """Определяет настройки модели Comment."""

        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        """Определяет отображение модели Comment."""
        return self.text[:15]
