from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from core.views import EntityTagsView, EntityViewSet

from .models import Action, ActionTags
from .serializers import (
    ActionSerializer,
    ActionSuggestionChangesSerializer,
    ActionSuggestionSerializer,
    ActionTagsSerializer,
)


class ActionViewSet(EntityViewSet):
    """Obtenha uma ação por seu ID."""  # swagger

    serializer_class = ActionSerializer
    model = Action
    suggestion_serializer_class = ActionSuggestionSerializer
    suggestion_change_serializer_class = ActionSuggestionChangesSerializer


class ActionTagsViewSet(EntityTagsView):
    """Obtenha uma tag por seu slug."""  # swagger

    model = ActionTags
    tags_serializer_class = ActionTagsSerializer

    @swagger_auto_schema(responses={200: ActionTagsSerializer})
    @action(methods=["GET"], detail=False)
    def main(self, *args, **kwargs):
        """Obtenha as tags "principais" e suas respectivas tags "filhas"."""  # swagger
        return super().main(*args, **kwargs)
