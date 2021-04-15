from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from core.views import EntityTagsView, EntityViewSet

from .models import Quote, QuoteTags
from .serializers import (
    QuoteSerializer,
    QuoteSuggestionChangesSerializer,
    QuoteSuggestionSerializer,
    QuoteTagsSerializer,
)


class QuoteViewSet(EntityViewSet):
    """Obtenha uma declaração por seu ID."""

    serializer_class = QuoteSerializer
    model = Quote
    suggestion_serializer_class = QuoteSuggestionSerializer
    suggestion_change_serializer_class = QuoteSuggestionChangesSerializer


class QuoteTagsViewSet(EntityTagsView):
    """Obtenha uma tag por seu slug."""  # swagger

    model = QuoteTags
    tags_serializer_class = QuoteTagsSerializer

    @swagger_auto_schema(responses={200: QuoteTagsSerializer})
    @action(methods=["GET"], detail=False)
    def main(self, *args, **kwargs):
        """Obtenha as tags "principais" e suas respectivas tags "filhas"."""
        return super().main(*args, **kwargs)
