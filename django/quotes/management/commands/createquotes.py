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
        dir_path = os.path.join(__location__, "../../..", "data")

        with open(
            os.path.join(dir_path, "quotes_tags.json"),
            encoding="utf-8",
        ) as tags_file:
            tags = json.load(tags_file)
            for tag in tags:
                del tag["slug"]
                childrens = tag.pop("childrens")
                tag_obj = QuoteTags.objects.create(**tag)
                for children in childrens:
                    del children["slug"]
                    QuoteTags.objects.create(**children, parent=tag_obj)

        with open(
            os.path.join(dir_path, "quotes.json"),
            encoding="utf-8",
        ) as quotes_file:
            quotes = json.load(quotes_file)
            for quote in quotes:
                quote_tags = quote.pop("tags")
                quote_obj = Quote.objects.create(
                    **{
                        **quote,
                        "date": datetime.strptime(quote.pop("date"), "%d/%m/%Y"),
                    }
                )
                quote_obj.tags.add(*quote_tags)  # taggit needs a pk
                quote_obj.save()
