from rest_framework import serializers

from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Review."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=("author", "title",),
                message="Можно оставить только 1 отзыв!"
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Comment