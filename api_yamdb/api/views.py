from rest_framework import viewsets
from reviews.models import Review, Comment, Title

from .permissions import IsModeratorOrAuthorOrReadonly
from .serializers import ReviewSerializer, CommentSerializer, TitleSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAuthorOrReadonly,)
    def get_title(self):
        return Title.objects.get(pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorOrAuthorOrReadonly,)

    def get_review(self):
        return Review.objects.get(pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
