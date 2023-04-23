"""Модуль содержит view для приложения api."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status, serializers, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrStaffOrReadOnly,
    IsAdminOnly,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
    GetTokenSerializer,
    SignupSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Category, Genre, Title, Review

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD операции для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (permissions.IsAuthenticated, IsAdminOnly)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        """Определяет permissions в зависимости от метода."""
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(["get", "patch", "delete"], detail=False)
    def me(self, request):
        """Функция для обработки 'users/me' endpoint."""
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save(role=self.request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = UserSerializer(request.user)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.all().order_by("id")
    serializer_class = TitleWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """Функция определяет сериалайзер в зависимости от метода."""
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


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
            **serializer.validated_data,
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для просмотра и редактирования Отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_title(self):
        """Определяет функцию для получения title_id из url."""
        return Title.objects.get(pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        """Переопределяет queryset в зависимости от title_id."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Переопределяет действия при создания записи.

        Обновляет поля author и title произведения
        для сохраняемой записи.
        """
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для создания и редактирования комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_review(self):
        """Определяет функцию для получения review_id из url."""
        return Review.objects.get(pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        """Переопределяет queryset в зависимости от review_id."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Переопределяет действия при создания записи.

        Обновляет поля author и pk review для сохраняемой записи.
        """
        serializer.save(author=self.request.user, pk=self.get_review())
