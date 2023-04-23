"""Модуль содержит настройки для панели администратора приложения reviews."""
from django.contrib import admin
from reviews.models import Comment, Category, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    """Настройки для панели администратора модели User."""

    list_display = (
        "username",
        "is_admin",
        "role",
        "first_name",
        "last_name",
        "email",
        "bio",
    )
    search_fields = ("username", "role")
    list_filter = ("role",)
    empty_value_display = "-пусто-"
    list_editable = ("role", "is_admin")


class CategoryAdmin(admin.ModelAdmin):
    """Настройки для панели администратора модели Category."""

    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)


class GenreAdmin(admin.ModelAdmin):
    """Настройки для панели администратора модели Genre."""

    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)


class TitleAdmin(admin.ModelAdmin):
    """Настройки для панели администратора модели Title."""

    list_display = ("name", "year", "description", "category")
    search_fields = ("name",)
    list_filter = ("year", "genre", "category")


class CommentAdmin(admin.ModelAdmin):
    """Настройки админ-панели для комментариев."""

    list_display = (
        "id",
        "text",
        "author",
        "created",
    )
    search_fields = (
        "text",
        "author",
    )
    list_filter = (
        "text",
        "author",
        "created",
    )


class ReviewAdmin(admin.ModelAdmin):
    """Настройки админ-панели для отзывов."""

    list_display = (
        "id",
        "text",
        "author",
        "score",
        "pub_date",
    )
    search_fields = (
        "text",
        "author",
        "pub_date",
    )
    list_filter = (
        "text",
        "author",
        "pub_date",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
