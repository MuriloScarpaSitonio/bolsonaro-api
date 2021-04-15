from __future__ import annotations

from collections import OrderedDict
from typing import Any

from rest_framework.serializers import ValidationError

from core.serializers import (
    AbstractSerializer,
    AbstractSuggestionSerializer,
    AbstractTagsSerializer,
)

from .models import Quote, QuoteSuggestion, QuoteSuggestionChanges, QuoteTags


class QuoteSerializer(AbstractSerializer):
    class Meta(AbstractSerializer.Meta):
        model = Quote


class QuoteTagsSerializer(AbstractTagsSerializer):
    class Meta(AbstractTagsSerializer.Meta):
        model = QuoteTags


class QuoteSuggestionSerializer(AbstractSuggestionSerializer):
    class Meta(AbstractSuggestionSerializer.Meta):
        model = QuoteSuggestion

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """
        Raises:
            ValidationError: Se o usuário marcar o campo is_fake_news como True e
                não preencher o campo fake_news_source.
            ValidationError: Se o usuário não marcar o campo is_fake_news como True e
                preencher o campo fake_news_source.
        """
        super().validate(attrs)

        if attrs.get("is_fake_news") and not attrs.get("fake_news_source"):
            raise ValidationError(
                {
                    "fake_news_source": (
                        "Se é uma fake news, "
                        "forneça uma fonte que comprove a falsidade da declaração."
                    )
                }
            )

        if not attrs.get("is_fake_news") and attrs.get("fake_news_source"):
            raise ValidationError(
                {
                    "is_fake_news": (
                        "Se há uma fonte compravando que é uma fake news, "
                        "passe o parâmetro is_fake_news como True."
                    )
                }
            )
        return attrs


class QuoteSuggestionChangesSerializer(QuoteSuggestionSerializer):
    class Meta(QuoteSuggestionSerializer.Meta):
        model = QuoteSuggestionChanges

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        """
        Raises:
            ValidationError: Se o usuário sugerir mudanças sem alterar nenhum campo
                da declaração original.
        """
        super().validate(attrs)

        changes = []
        for attr, value in attrs.items():
            if attr in ("original_quote", "user_email", "justification"):
                continue

            if attr == "tags":
                original_value = sorted(list(attrs["original_quote"].tags_names))
                value = sorted(value)
            else:
                original_value = getattr(attrs["original_quote"], attr)

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
