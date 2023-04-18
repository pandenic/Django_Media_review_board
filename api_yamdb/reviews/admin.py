"""Модуль содержит настройки для панели администратора приложения reviews."""
from django.contrib import admin

from reviews.models import User


class UserAdmin(admin.ModelAdmin):
    """Настройки для панели администратора модели User."""

    list_display = (
        "username",
        "role",
        "first_name",
        "last_name",
        "email",
        "bio",
    )
    search_fields = ("username", "role")
    list_filter = ("role",)
    empty_value_display = "-пусто-"
    list_editable = ("role",)


admin.site.register(User, UserAdmin)
