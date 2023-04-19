from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'title',
        'score'
    )
    search_fields = ('author', 'text')
    list_filter = ('pub_date',)

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'created',
    )
    search_fields = ('author', 'text',)
    list_filter = ('created',)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)