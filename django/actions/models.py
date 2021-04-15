from datetime import date
from typing import List

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase

from core.models import AbstractEntity, AbstractGroupedTag
from django.db import models


class ActionTags(AbstractGroupedTag):
    class Meta:
        verbose_name = "Marcador de ação"
        verbose_name_plural = "Marcadores de ações"

    @property
    def childrens(self) -> models.query.QuerySet:
        return ActionTags.objects.filter(parent=self)


class TaggedAction(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ActionTags,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_items",
    )


class AbstractAction(AbstractEntity):
    """
    Classe que modela uma ação.

    Args:
        tags (taggit.managers._TaggableManager): Modelo que gerencia as tags da ação.
    """

    tags = TaggableManager(through=TaggedAction)

    class Meta:
        abstract = True

    @property
    def tags_names(self) -> models.query.QuerySet:
        return self.tags.names()


class Action(AbstractAction):
    class Meta:
        verbose_name = "Ação"
        verbose_name_plural = "Ações"


class ActionSuggestion(AbstractAction):
    """
    Classe que modela uma sugestão de uma nova ação.

    Args:
        user_email (str): O e-mail do usuário que sugeriu a mudança.
    """

    user_email = models.EmailField(verbose_name="E-mail do usuário")

    class Meta:
        verbose_name = "Sugestão de ação"
        verbose_name_plural = "Sugestões de ações"

    def accept(self) -> Action:
        """
        Método que é responsável por aceitar a sugestão do usuário.
        Logo, o que este método faz nada mais é do que criar um objeto Action da sugestão.

        Returns:
            (Action): Objeto que representa uma ação.
        """
        action = Action.objects.create(
            description=self.description,
            source=self.source,
            date=self.date,
            date_is_estimated=self.date_is_estimated,
            additional_infos=self.additional_infos,
        )
        action.tags.add(*self.tags_names)
        action.save()
        return action


class ActionSuggestionChanges(AbstractAction):
    """
    Classe que modela uma sugestão de mudança em uma ação.

    Args:
        original_action (Action): A ação original;
        user_email (str): O e-mail do usuário que sugeriu a mudança;
        justification (str): A justificativa dada pela usuário para a mudança.
    """

    original_action = models.ForeignKey(Action, on_delete=models.CASCADE)
    user_email = models.EmailField(verbose_name="E-mail do usuário")
    justification = models.TextField(verbose_name="Justificativa da mudança")

    class Meta:
        verbose_name = "Sugestão de mudanças em ação"
        verbose_name_plural = "Sugestões de mudanças em ações"

    @property
    def original_action_description(self) -> str:
        return self.original_action.description

    original_action_description.fget.description = "Descrição (original)"  # type: ignore

    @property
    def original_action_source(self) -> str:
        return self.original_action.source

    original_action_source.fget.description = "Fonte (original)"  # type: ignore

    @property
    def original_action_date(self) -> date:
        return self.original_action.date

    original_action_date.fget.description = "Data (original)"  # type: ignore

    @property
    def original_action_date_is_estimated(self) -> bool:
        return self.original_action.date_is_estimated

    original_action_date_is_estimated.fget.description = (  # type: ignore
        "A data é estimada? (original)"
    )

    @property
    def original_action_additional_infos(self) -> str:
        return self.original_action.additional_infos

    original_action_additional_infos.fget.description = (  # type: ignore
        "Informações adicionais (original)"
    )

    @property
    def original_action_tags(self) -> str:
        return ", ".join(self.original_action.tags_names)

    original_action_tags.fget.description = "Marcadores (original)"  # type: ignore

    def _get_changes_fields_names(self) -> List[str]:
        """
        Método que obtém os nomes dos campos que tiveram mudança.

        Returns:
            changes (List[str, ...]): Lista com os nomes dos campos que tiveram mudança.
        """
        changes = []
        for field in self.original_action._meta.get_fields():
            if field.name in ("id", "tagged_items", "actionsuggestionchanges"):
                continue

            if field.name == "tags":
                original_value = sorted(list(self.original_action.tags_names))
                new_value = sorted(list(self.tags_names))
            else:
                original_value = getattr(self.original_action, field.name)
                new_value = getattr(self, field.name)

            if original_value != new_value:
                changes.append(field.name)

        return changes

    def accept(self) -> Action:
        """
        Método que é responsável por aceitar a sugestão de mudança do usuário.
        Logo, o que este método faz nada mais é do que alterar o objeto Action original com
        as sugestões propostas.

        Returns:
            (Action): Objeto que representa uma ação.
        """
        fields = self._get_changes_fields_names()
        for field in fields:
            if field == "tags":
                self.original_action.tags.clear()
                self.original_action.save()
                self.original_action.tags.add(*self.tags_names)
                fields.remove(field)  # m2m
            else:
                setattr(self.original_action, field, getattr(self, field))

        self.original_action.save(update_fields=fields)
        return self.original_action
