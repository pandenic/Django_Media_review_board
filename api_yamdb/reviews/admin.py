from django.contrib import admin

from .models import Comment, Review

class CommentAdmin(admin.ModelAdmin):
    """
    Настройка администратора для раздела комментарии.
    """

    list_display = (
        'id',
        'text',
        'author',
    )
    list_filter = ('text', 'author',)
    search_fields = ('text',)

class ReviewAdmin(admin.ModelAdmin):
    """
    Настройки администратора для раздела отзывы.
    """
    
    list_display = (
        'id',
        'text',
        'author',
        'score',
    )
    list_filter = ('text', 'author',)
    search_fields = ('text',)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
