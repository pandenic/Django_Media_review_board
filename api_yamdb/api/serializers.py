"""Модуль содержит описание serializers для приложения api."""
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализирует модель user."""

    class Meta:
        """Определяет настройки сериалайзера UserSerializer."""

        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        """Определяет настройки сериалайзера CategorySerializer."""

        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        """Определяет настройки сериалайзера GenreSerializer."""

        model = Genre
        exclude = ("id",)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для записи."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field="slug",
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug",
    )

    class Meta:
        """Определяет настройки сериалайзера TitleWriteSerializer."""

        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, data):
        """Проверяет год при сериализации создания записи в модель Title."""
        current_year = timezone.now().year
        if data > current_year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего.",
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Определяет настройки сериалайзера TitleReadSerializer."""

        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class GetTokenSerializer(serializers.Serializer):
    """Сериализирует получение токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class SignupSerializer(serializers.Serializer):
    """Сериализирует регистрацию для получения confirmation code."""

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate(self, attrs):
        """Проверяет входные данные при сериализации регистрации."""
        username = attrs["username"]
        email = attrs["email"]
        if username == "me":
            raise serializers.ValidationError(
                "Нельзя использовать me в качестве имени пользователя",
            )
        user_list = User.objects.filter(username=username)
        if user_list.exists() and user_list[0].email != email:
            raise serializers.ValidationError(
                "Нельзя использовать существующеe имя пользователя",
            )
        user_list = User.objects.filter(email=email)
        if user_list.exists() and user_list[0].username != username:
            raise serializers.ValidationError(
                "Нельзя использовать email существующего пользователя",
            )
        return attrs


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
