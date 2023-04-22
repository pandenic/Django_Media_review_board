"""Модуль, в котором содержатся url для приложения api."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
    )
from api.routers import CustomUserRouter
from api.views import UserViewSet, get_token, sign_up

app_name = "api"

router = SimpleRouter()
router.register(
    "titles",
    TitleViewSet,
    basename="titles",
)
router.register("categories", CategoryViewSet, basename="categories")
router.register(
    "genres",
    GenreViewSet,
    basename="genres",
)

user_router = CustomUserRouter()
user_router.register(
    "users",
    UserViewSet,
    basename="users",
)

router_v1 = DefaultRouter()
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)

v1 = [
    path("", include(router_v1.urls)),
    path("", include(router.urls)),
    path("", include(user_router.urls)),
    path("auth/token/", get_token, name="token_obtain"),
    path("auth/signup/", sign_up, name="sign_up"),
]

urlpatterns = [path("v1/", include(v1))]
