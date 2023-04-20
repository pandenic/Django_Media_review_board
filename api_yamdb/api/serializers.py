"""Модуль содержит описание serializers для приложения api."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализирует модель user."""

    class Meta:
        """Metaclass of PostSerializer contains model link and fields tuple."""

        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class GetTokenSerializer(serializers.Serializer):
    """Сериализирует получение токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class SignupSerializer(serializers.Serializer):
    """Сериализирует регистрацию для получения confirmation code."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
