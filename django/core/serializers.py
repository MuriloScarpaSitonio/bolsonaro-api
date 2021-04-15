from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, List, Union

from drf_recaptcha.fields import ReCaptchaV2Field
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from taggit.models import Tag

from django.conf import settings

from actions.models import ActionSuggestion, ActionSuggestionChanges, ActionTags
from quotes.models import QuoteSuggestion, QuoteSuggestionChanges, QuoteTags


class AbstractSerializer(serializers.ModelSerializer):
    tags = serializers.ReadOnlyField(source="tags_names")
    date = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug")


class AbstractTagsSerializer(serializers.ModelSerializer):
    """
    Classe que representa o modelo 'Quote/Action'Tags com a serialização
    das tags 'filhas'.
    """

    childrens = serializers.SerializerMethodField()

    class Meta:
        fields = ("name", "slug", "childrens")

    @swagger_serializer_method(serializer_or_field=TagSerializer)
    def get_childrens(self, tag: Union[ActionTags, QuoteTags]) -> List[Dict[str, str]]:
        return TagSerializer(tag.childrens, many=True).data


class AbstractSuggestionSerializer(serializers.ModelSerializer):
    """
    Classe que serializa um modelo para sugestão de novas ações/declarações.

    Raises:
        serializers.ValidationError: Se o usuário sugerir uma tag que não está cadastrada.
    """

    tags = serializers.ListField()
    recaptcha = ReCaptchaV2Field()

    class Meta:
        fields = "__all__"

    def create(
        self, validated_data: Dict[str, Any]
    ) -> Union[
        ActionSuggestion,
        ActionSuggestionChanges,
        QuoteSuggestion,
        QuoteSuggestionChanges,
    ]:
        tags = validated_data.pop("tags", [])
        suggested = self.Meta.model.objects.create(**validated_data)  # type: ignore
        suggested.tags.add(*tags)
        suggested.save()
        return suggested

    def validate(self, attrs: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        attrs.pop("recaptcha", "")
        invalid_tags = []
        for tag in attrs.get("tags", []):
            qs = self.Meta.model.tags.through.tag_model().objects.filter(name=tag)  # type: ignore
            if not qs.exists():
                invalid_tags.append(f"'{tag}'")

        if invalid_tags:
            if len(invalid_tags) > 1:
                invalid_tags_str = (
                    ", ".join(invalid_tags[:-1]) + " e " + invalid_tags[-1]
                )
            else:
                invalid_tags_str = invalid_tags[0]
            raise serializers.ValidationError(
                {
                    "tags": (
                        f"A(s) tag(s) {invalid_tags_str} "
                        "não consta(m) na nossa base e por isso é(são) considerada(s) inválida(s). "
                        "Se você pensa que ela(s) é(são) imprescindível(is) contate-nos por "
                        f"e-mail ({settings.EMAIL_HOST_USER})."
                    )
                }
            )

        return attrs


class EntityCountSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    total = serializers.IntegerField()
