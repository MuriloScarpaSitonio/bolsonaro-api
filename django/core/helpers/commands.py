import json
from datetime import datetime
from typing import Union

from actions.models import Action, ActionTags
from quotes.models import Quote, QuoteTags


def create_entities(
    tags_file_path: str,
    tags_model: Union[ActionTags, QuoteTags],
    entities_file_file_path: str,
    entity_model: Union[Action, Quote],
) -> None:
    """Função que cria entidades e tags com base em arquivos json.

    Args:
        tags_file_path (str): Arquivo com informações das tags;
        tags_model (Union[ActionTags, QuoteTags]): O modelo da tag;
        entities_file_file_path (str): Arquivo com informações das entidades;
        entity_model (Union[Action, Quote]): O model da entidade.
    """
    with open(tags_file_path, encoding="utf-8") as tags_file:
        for tag in json.load(tags_file):
            del tag["slug"]
            childrens = tag.pop("childrens")
            tag_obj, _ = tags_model.objects.get_or_create(**tag)
            for children in childrens:
                del children["slug"]
                tags_model.objects.get_or_create(**children, parent=tag_obj)

    with open(entities_file_file_path, encoding="utf-8") as entities_file:
        for entity in json.load(entities_file):
            entity_tags = entity.pop("tags")
            entity_obj, created = entity_model.objects.get_or_create(
                **{
                    **entity,
                    "date": datetime.strptime(entity.pop("date"), "%d/%m/%Y"),
                }
            )
            if created:
                entity_obj.tags.add(*entity_tags)  # taggit needs a pk
                entity_obj.save()
