import json
import os
from datetime import datetime

from actions.models import Action, ActionTags
from django.core.management.base import BaseCommand

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    """Comando que cria as ações e tags contidas nos arquivos actions.json e actions_tags.json

    >>> python manage.py createactions
    """

    def handle(self, *args, **options):
        dir_path = os.path.join(__location__, "../../..", "data")

        with open(
            os.path.join(dir_path, "actions_tags.json"),
            encoding="utf-8",
        ) as tags_file:
            tags = json.load(tags_file)
            for tag in tags:
                del tag["slug"]
                childrens = tag.pop("childrens")
                tag_obj = ActionTags.objects.create(**tag)
                for children in childrens:
                    del children["slug"]
                    ActionTags.objects.create(**children, parent=tag_obj)

        with open(
            os.path.join(dir_path, "actions.json"),
            encoding="utf-8",
        ) as actions_file:
            actions = json.load(actions_file)
            for action in actions:
                action_tags = action.pop("tags")
                action_obj = Action.objects.create(
                    **{
                        **action,
                        "date": datetime.strptime(action.pop("date"), "%d/%m/%Y"),
                    }
                )
                action_obj.tags.add(*action_tags)  # taggit needs a pk
                action_obj.save()
