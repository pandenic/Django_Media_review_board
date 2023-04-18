from django.contrib import admin

from reviews.models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)


class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "description", "category")
    search_fields = ("name",)
    list_filter = ("year", "genre", "category")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
