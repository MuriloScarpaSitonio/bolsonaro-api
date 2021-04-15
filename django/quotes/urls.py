from rest_framework import routers

from django.urls import include, path

from .views import QuoteTagsViewSet, QuoteViewSet

quotes_router = routers.DefaultRouter(trailing_slash=False)
quotes_router.register(prefix=r"quotes", viewset=QuoteViewSet, basename="actions")

quotes_tags_router = routers.DefaultRouter(trailing_slash=False)
quotes_tags_router.register(
    prefix=r"quotes/tags", viewset=QuoteTagsViewSet, basename="quotes_tags"
)

urlpatterns = [
    path("", include(quotes_tags_router.urls)),
    path("", include(quotes_router.urls)),
]
