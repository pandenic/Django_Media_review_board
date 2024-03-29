"""Модуль содержит view для приложения api."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status, serializers, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
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
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
    ENDPOINT_ME,
)
from api.errors import ErrorMessage
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class HTTPMethod:
    """Определяет HTTP методы для работы viewsets."""

    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"


class UserViewSet(viewsets.ModelViewSet):
    """Выполняет CRUD операции для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (permissions.IsAuthenticated, IsAdminOnly)
    http_method_names = (
        HTTPMethod.GET,
        HTTPMethod.POST,
        HTTPMethod.PATCH,
        HTTPMethod.DELETE,
    )

    def get_permissions(self):
        """Определяет permissions в зависимости от метода."""
        if self.action == ENDPOINT_ME:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(
        (HTTPMethod.GET, HTTPMethod.PATCH, HTTPMethod.DELETE),
        detail=False,
    )
    def me(self, request):
        """Функция для обработки 'users/me' endpoint."""
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    queryset = (
        Title.objects.annotate(
            rating=Avg(
                "reviews__score",
            ),
        )
        .all()
        .order_by("id")
    )
    serializer_class = TitleWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """Функция определяет сериалайзер в зависимости от метода."""
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


@api_view(("POST",))
@permission_classes((permissions.AllowAny,))
def get_token(request):
    """Функция получения нового токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(
        user,
        serializer.validated_data["confirmation_code"],
    ):
        raise serializers.ValidationError(
            ErrorMessage.INVALID_CONFIRMATION_CODE_ERROR,
        )

    token = RefreshToken.for_user(user)

    return Response(
        {"token": str(token.access_token)},
        status=status.HTTP_200_OK,
    )


@api_view(("POST",))
@permission_classes((permissions.AllowAny,))
def sign_up(request):
    """Функция регистрации и получения письма с confirmation code."""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, created = User.objects.get_or_create(
        **serializer.validated_data,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "yamdb код подтверждения",
        f"Код подтверждения: {confirmation_code}",
        settings.EMAIL_BACKEND,
        (user.email,),
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для просмотра и редактирования Отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    )

    def get_title(self):
        """Определяет функцию для получения title_id из url."""
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    )

    def get_review(self):
        """Определяет функцию для получения title_id и review_id."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        """Переопределяет queryset в зависимости от review_id."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """
        Переопределяет действия при создания записи.

        Обновляет поля author и pk review для сохраняемой записи.
        """
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )
