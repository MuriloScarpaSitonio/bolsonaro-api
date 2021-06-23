import os

from django.core.management.base import BaseCommand

from quotes.models import Quote, QuoteTags
from core.helpers.commands import create_entities

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    """Comando que cria as ações e tags contidas nos arquivos quotes.json e quotes_tags.json

    >>> python manage.py create_quotes
    """

    help = "Creates quotes and its tags, if it doesn't exist, based on json files"

    def add_arguments(self, parser):
        dir_path = os.path.join(__location__, "../../..", "data")
        parser.add_argument(
            "--quotes-json",
            help="The full path to the quotes json file",
            default=os.path.join(dir_path, "quotes.json"),
        )
        parser.add_argument(
            "--tags-json",
            help="The full path to the quotes tags json file",
            default=os.path.join(dir_path, "quotes_tags.json"),
        )

    def handle(self, *args, **options):
        print("Creating quotes and its tags...")
        create_entities(
            tags_file_path=options["tags_json"],
            tags_model=QuoteTags,
            entities_file_file_path=options["quotes_json"],
            entity_model=Quote,
        )
        print("Quotes and tags created!")
