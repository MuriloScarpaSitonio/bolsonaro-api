from rest_framework import routers

from django.urls import include, path

from .views import ActionTagsViewSet, ActionViewSet

actions_router = routers.DefaultRouter(trailing_slash=False)
actions_router.register(prefix=r"actions", viewset=ActionViewSet, basename="actions")

actions_tags_router = routers.DefaultRouter(trailing_slash=False)
actions_tags_router.register(
    prefix=r"actions/tags",
    viewset=ActionTagsViewSet,
    basename="actions_tags",
)

urlpatterns = [
    path("", include(actions_tags_router.urls)),
    path("", include(actions_router.urls)),
]
