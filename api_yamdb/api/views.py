"""Модуль содержит view для приложения api."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.pagination import UserPagination
from api.serializers import (GetTokenSerializer, SignupSerializer,
                             UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD операции для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    lookup_field = "username"

    @action(["get", "patch"], detail=False)
    def me(self, request):
        """Функция для обработки 'users/me' endpoint."""
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(request.user)

        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Функция получения нового токена."""
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(
            user,
            serializer.validated_data["confirmation_code"],
        ):
            raise serializers.ValidationError("Invalid confirmation code")

        token = RefreshToken.for_user(user)

        return Response(
            {"token": str(token.access_token)},
            status=status.HTTP_200_OK,
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def sign_up(request):
    """Функция регистрации и получения письма с confirmation code."""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user, created = User.objects.get_or_create(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "yamdb код подтверждения",
            f"Код подтверждения: {confirmation_code}",
            "yamdb@yamdb.com",
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
