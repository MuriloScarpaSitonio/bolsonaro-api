from taggit.models import TagBase

from django.core.validators import URLValidator
from django.db import models


class AbstractGroupedTag(TagBase):
    """
    Classe base para as tags dos modelos Quote e Action.
    Aqui estendemos a biblioteca taggit para criar uma hierarquia entre as tags.
    """

    slug = models.SlugField(unique=True, blank=True, max_length=100)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="child",
    )

    class Meta:
        abstract = True


class AbstractEntity(models.Model):
    """
    Classe que modela uma entidade (ação ou declaração).

    Args:
        description (str): Uma descrição da ação ou declaração;
        source (str): O URL de uma fonte que contenha informações da ação ou declaração;
        date (datetime): A data da ação ou declaração;
        date_is_estimated (bool): True, se a data for estimada. False, do contrário;
        additional_infos (str): Informações adicionais da ação ou declaração, se aplicável.
    """

    description = models.TextField(verbose_name="Descrição")
    source = models.CharField(
        max_length=1000,
        verbose_name="Fonte",
        validators=[URLValidator(message="URL inválido")],
    )
    date = models.DateField(verbose_name="Data")
    date_is_estimated = models.BooleanField(
        default=False,
        verbose_name="A data é estimada?",
    )
    additional_infos = models.TextField(
        blank=True,
        verbose_name="Informações adicionais",
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.description
