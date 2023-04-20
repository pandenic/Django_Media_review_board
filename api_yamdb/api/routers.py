"""Модуль описывает классы роутеров."""

from rest_framework.routers import Route, DynamicRoute, SimpleRouter


class CustomUserRouter(SimpleRouter):

    routes = [
        Route(
            url=r"^{prefix}/$",
            mapping={
                "get": "list",
                "post": "create",
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"}
        ),
        Route(
            url=r"^{prefix}/{lookup}/$",
            mapping={
                "get": "retrieve",
                "patch": "update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Detail"}
        ),
        DynamicRoute(
            url=r"^{prefix}/{url_path}/$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={}
        ),
    ]