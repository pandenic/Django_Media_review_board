"""Модуль содержит описание serializers для приложения api."""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from api.errors import ErrorMessage

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализирует модель user."""

    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254,
    )

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
        queryset=Genre.objects.all(),
        many=True,
        slug_field="slug",
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
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
                ErrorMessage.ME_AS_USERNAME_ERROR,
            )
        user_list = User.objects.filter(username=username)
        if user_list.exists() and user_list[0].email != email:
            raise serializers.ValidationError(
                ErrorMessage.EXISTS_EMAIL_ERROR,
            )
        user_list = User.objects.filter(email=email)
        if user_list.exists() and user_list[0].username != username:
            raise serializers.ValidationError(
                ErrorMessage.EXISTS_USERNAME_ERROR,
            )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Review."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        """Определяет настройки сериалайзера ReviewSerializer."""

        fields = "__all__"
        model = Review

    def validate(self, data):
        """Проверяет, что нельзя оставить больше одного отзыва."""
        request = self.context["request"]
        author = request.user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == "POST"
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                "Можно написать только один отзыв!",
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        """Определяет настройки сериалайзера CommentSerializer."""

        fields = "__all__"
        model = Comment
