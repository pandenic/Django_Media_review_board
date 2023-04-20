"""Модуль содержит описание serializers для приложения api."""
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализирует модель user."""

    class Meta:
        """Metaclass of PostSerializer contains model link and fields tuple."""

        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
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
