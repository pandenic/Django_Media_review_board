from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)


class Review(models.Model):
    """Модель отзывов на произведения."""
    text = models.CharField(
        max_length=256,
        verbose_name='Текст отзыва',
        help_text = 'Введите текст отзыва'
        )
    author = models.ForeignKey(
        User,
        related_name='reviewer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Произведение'
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        help_text='Укажите оценку от 1 до 10',
        validators=[
            MinValueValidator(
                1,
                message='Оценка ниже допустимой!'
            ),
            MaxValueValidator(
                10,
                message='Оценка выше допустимой!'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text[:15]

class Comment(models.Model):
    """Модель комментариев к отзывам."""

    text = models.CharField(
        max_length=256,
        verbose_name='Текст комментария',
        help_text='Текст комментария к отзыву'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Автор комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии',
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[:15]

