"""Модуль содержит описание serializers для приложения api."""
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from reviews.models import Category, Genre, Title

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Сериализирует модель user."""

    class Meta:
        """Metaclass of PostSerializer contains model link and fields tuple."""

        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        exclude = ("id",)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для записи."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field="slug"
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, data):
        current_year = timezone.now().year
        if data > current_year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
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

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
