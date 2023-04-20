from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review, Comment, Title

from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer, TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Viewset для просмотра и редактирования Отзывов.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    
    def get_title(self):
        return Title.objects.get(pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset для создания и редактирования комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly)

    def get_review(self):
        return Review.objects.get(pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            pk=self.get_review()
        )
