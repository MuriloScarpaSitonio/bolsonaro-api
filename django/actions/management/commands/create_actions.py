import os

from django.core.management.base import BaseCommand

from actions.models import Action, ActionTags
from core.helpers.commands import create_entities

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    """Comando que cria as ações e tags contidas nos arquivos actions.json e actions_tags.json

    >>> python manage.py create_actions
    """

    help = "Creates actions and its tags, if it doesn't exist, based on json files"

    def add_arguments(self, parser):
        dir_path = os.path.join(__location__, "../../..", "data")
        parser.add_argument(
            "--actions-json",
            help="The full path to the actions json file",
            default=os.path.join(dir_path, "actions.json"),
        )
        parser.add_argument(
            "--tags-json",
            help="The full path to the actions tags json file",
            default=os.path.join(dir_path, "actions_tags.json"),
        )

    def handle(self, *args, **options):
        print("Creating actions and its tags...")
        create_entities(
            tags_file_path=options["tags_json"],
            tags_model=ActionTags,
            entities_file_file_path=options["actions_json"],
            entity_model=Action,
        )
        print("Actions and tags created!")
