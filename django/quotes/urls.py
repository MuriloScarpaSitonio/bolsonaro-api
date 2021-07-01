from rest_framework import routers

from .views import QuoteTagsViewSet, QuoteViewSet

quotes_router = routers.DefaultRouter(trailing_slash=False)
quotes_router.register(prefix=r"quotes", viewset=QuoteViewSet, basename="actions")

quotes_tags_router = routers.DefaultRouter(trailing_slash=False)
quotes_tags_router.register(
    prefix=r"quotes/tags", viewset=QuoteTagsViewSet, basename="quotes_tags"
)

urlpatterns = quotes_tags_router.urls + quotes_router.urls
