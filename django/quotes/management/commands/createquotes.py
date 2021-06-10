import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from quotes.models import Quote, QuoteTags

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    """Comando que cria as ações e tags contidas nos arquivos quotes.json e quotes_tags.json

    >>> python manage.py createquotes
    """

    def handle(self, *args, **options):
        print("Creating quotes and its tags...")
        dir_path = os.path.join(__location__, "../../..", "data")

        with open(
            os.path.join(dir_path, "quotes_tags.json"), encoding="utf-8"
        ) as tags_file:
            for tag in json.load(tags_file):
                del tag["slug"]
                childrens = tag.pop("childrens")
                tag_obj, _ = QuoteTags.objects.get_or_create(**tag)
                for children in childrens:
                    del children["slug"]
                    QuoteTags.objects.get_or_create(**children, parent=tag_obj)

        with open(
            os.path.join(dir_path, "quotes.json"), encoding="utf-8"
        ) as quotes_file:
            for quote in json.load(quotes_file):
                quote_tags = quote.pop("tags")
                quote_obj, created = Quote.objects.get_or_create(
                    **{
                        **quote,
                        "date": datetime.strptime(quote.pop("date"), "%d/%m/%Y"),
                    }
                )
                if created:
                    quote_obj.tags.add(*quote_tags)  # taggit needs a pk
                    quote_obj.save()

        print("Quotes and tags created!")
