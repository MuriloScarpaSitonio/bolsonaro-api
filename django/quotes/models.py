from datetime import date
from typing import List

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase

from core.models import AbstractEntity, AbstractGroupedTag
from django.core.validators import URLValidator
from django.db import models


class QuoteTags(AbstractGroupedTag):
    class Meta:
        verbose_name = "Marcador de declaração"
        verbose_name_plural = "Marcadores de declarações"

    @property
    def childrens(self) -> models.query.QuerySet:
        return QuoteTags.objects.filter(parent=self)


class TaggedQuote(GenericTaggedItemBase):
    tag = models.ForeignKey(
        QuoteTags,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_items",
    )


class AbstractQuote(AbstractEntity):
    """
    Classe que modela uma declaração.

    Args:
        is_fake_news (bool): True, se a declaração for fake news. False, do contrário;
        fake_news_source (str): O URL que comprova que a declaração é fake news, se aplicável;
        tags (taggit.managers._TaggableManager): Modelo que gerencia as tags da declaração.
    """

    is_fake_news = models.BooleanField(verbose_name="Fake news?", default=False)
    fake_news_source = models.CharField(
        max_length=1000,
        blank=True,
        verbose_name="Fonte da fake news",
        validators=[URLValidator(message="URL inválido")],
    )
    tags = TaggableManager(through=TaggedQuote)

    class Meta:
        abstract = True

    @property
    def tags_names(self) -> models.query.QuerySet:
        return self.tags.names()


class Quote(AbstractQuote):
    class Meta:
        verbose_name = "Declaração"
        verbose_name_plural = "Declarações"


class QuoteSuggestion(AbstractQuote):
    """
    Classe responsável pela sugestões de declarações

    Args:
        user_email (str): O e-mail do usuário que sugeriu a mudança.
    """

    user_email = models.EmailField(verbose_name="E-mail do usuário")

    class Meta:
        verbose_name = "Sugestão de declaração"
        verbose_name_plural = "Sugestões de declarações"

    def accept(self) -> Quote:
        """
        Método que é responsável por aceitar a sugestão do usuário.
        Logo, o que este método faz nada mais é do que criar um objeto Quote da sugestão.

        Returns:
            (Quote): Objeto que representa uma declaração.
        """
        quote = Quote.objects.create(
            description=self.description,
            source=self.source,
            is_fake_news=self.is_fake_news,
            fake_news_source=self.fake_news_source,
            date=self.date,
            date_is_estimated=self.date_is_estimated,
            additional_infos=self.additional_infos,
        )
        quote.tags.add(*self.tags_names)
        quote.save()
        return quote


class QuoteSuggestionChanges(AbstractQuote):
    """
    Classe que modela uma sugestão de mudança em uma declaração.

    Args:
        original_quote (Quote): A declaração original;
        user_email (str): O e-mail do usuário que sugeriu a mudança;
        justification (str): A justificativa dada pela usuário para a mudança.
    """

    original_quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    user_email = models.EmailField(verbose_name="E-mail do usuário")
    justification = models.TextField(verbose_name="Justificativa da mudança")

    class Meta:
        verbose_name = "Sugestão de mudanças em declaração"
        verbose_name_plural = "Sugestões de mudanças em declarações"

    @property
    def original_quote_description(self) -> str:
        return self.original_quote.description

    original_quote_description.fget.description = "Declaração (original)"  # type: ignore

    @property
    def original_quote_source(self) -> str:
        return self.original_quote.source

    original_quote_source.fget.description = "Fonte (original)"  # type: ignore

    @property
    def original_quote_is_fake_news(self) -> bool:
        return self.original_quote.is_fake_news

    original_quote_is_fake_news.fget.description = "Fake news? (original)"  # type: ignore

    @property
    def original_quote_fake_news_source(self) -> str:
        return self.original_quote.fake_news_source

    original_quote_fake_news_source.fget.description = (  # type: ignore
        "Fonte da fake news (original)"
    )

    @property
    def original_quote_date(self) -> date:
        return self.original_quote.date

    original_quote_date.fget.description = "Data (original)"  # type: ignore

    @property
    def original_quote_date_is_estimated(self) -> bool:
        return self.original_quote.date_is_estimated

    original_quote_date_is_estimated.fget.description = (  # type: ignore
        "A data é estimada? (original)"
    )

    @property
    def original_quote_additional_infos(self) -> str:
        return self.original_quote.additional_infos

    original_quote_additional_infos.fget.description = (  # type: ignore
        "Informações adicionais (original)"
    )

    @property
    def original_quote_tags(self) -> str:
        return ", ".join(self.original_quote.tags_names)

    original_quote_tags.fget.description = "Marcadores (original)"  # type: ignore

    def _get_changes_fields_names(self) -> List[str]:
        """
        Método que obtém os nomes dos campos que tiveram mudança.

        Returns:
            changes (list): Lista com os nomes dos campos que tiveram mudança.
        """
        changes = []
        for field in self.original_quote._meta.get_fields():
            if field.name in ("id", "tagged_items", "quotesuggestionchanges"):
                continue

            if field.name == "tags":
                original_value = sorted(list(self.original_quote.tags_names))
                new_value = sorted(list(self.tags_names))
            else:
                original_value = getattr(self.original_quote, field.name)
                new_value = getattr(self, field.name)

            if original_value != new_value:
                changes.append(field.name)

        return changes

    def accept(self) -> Quote:
        """
        Método que é responsável por aceitar a sugestão de mudança do usuário.
        Logo, o que este método faz nada mais é do que alterar o objeto Quote original com
        as sugestões propostas.

        Returns:
            (Quote): Objeto que representa uma declaração.
        """
        fields = self._get_changes_fields_names()
        for field in fields:
            if field == "tags":
                self.original_quote.tags.clear()
                self.original_quote.save()
                self.original_quote.tags.add(*self.tags_names)
                fields.remove(field)  # m2m
            else:
                setattr(self.original_quote, field, getattr(self, field))

        self.original_quote.save(update_fields=fields)
        return self.original_quote
