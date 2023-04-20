"""Модуль, в котором содержатся url для приложения api."""
from django.urls import include, path

from api.routers import CustomUserRouter
from api.views import UserViewSet, get_token, sign_up

router = CustomUserRouter()
router.register(
    "users",
    UserViewSet,
    basename="users",
)

v1 = [
    path("", include(router.urls)),
    path("auth/token/", get_token, name="token_obtain"),
    path("auth/signup/", sign_up, name="sign_up"),
]

urlpatterns = [path("v1/", include(v1))]
