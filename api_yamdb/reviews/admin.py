from django.contrib import admin

from .models import Comment, Review

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
    )
    list_filter = ('text', 'author',)
    search_fields = ('text',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'score',
    )
    list_filter = ('text', 'author',)
    search_fields = ('text',)