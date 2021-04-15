from __future__ import annotations

from collections import OrderedDict
from typing import Any

from rest_framework.serializers import ValidationError

from core.serializers import (
    AbstractSerializer,
    AbstractSuggestionSerializer,
    AbstractTagsSerializer,
)

from .models import Action, ActionSuggestion, ActionSuggestionChanges, ActionTags


class ActionSerializer(AbstractSerializer):
    class Meta(AbstractSerializer.Meta):
        model = Action


class ActionTagsSerializer(AbstractTagsSerializer):
    class Meta(AbstractTagsSerializer.Meta):
        model = ActionTags


class ActionSuggestionSerializer(AbstractSuggestionSerializer):
    class Meta(AbstractSuggestionSerializer.Meta):
        model = ActionSuggestion


class ActionSuggestionChangesSerializer(ActionSuggestionSerializer):
    class Meta(ActionSuggestionSerializer.Meta):
        model = ActionSuggestionChanges

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """
        Raises:
            ValidationError: Se o usuário sugerir mudanças sem alterar nenhum campo
                da ação original.
        """
        super().validate(attrs)

        changes = []
        for attr, value in attrs.items():
            if attr in ("original_action", "user_email", "justification"):
                continue

            if attr == "tags":
                original_value = sorted(list(attrs["original_action"].tags_names))
                value = sorted(value)
            else:
                original_value = getattr(attrs["original_action"], attr)

            if value != original_value:
                changes.append(attr)

        if not changes:
            raise ValidationError(
                {
                    "errorMessage": (
                        "Todos os parâmetros da sugestão são iguais ao original! "
                        "Por favor, altere algum campo para que a sugestão torne-se válida."
                    )
                }
            )
        return attrs
