import json
import os
from datetime import datetime

import pytest
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient

from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest

from actions.models import Action, ActionSuggestion, ActionSuggestionChanges, ActionTags
from core.consts import API_BASE_URL
from quotes.models import Quote, QuoteSuggestion, QuoteSuggestionChanges, QuoteTags

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ActionFactory(DjangoModelFactory):
    class Meta:
        model = Action


class ActionSuggestionFactory(DjangoModelFactory):
    class Meta:
        model = ActionSuggestion


class ActionSuggestionChangesFactory(DjangoModelFactory):
    class Meta:
        model = ActionSuggestionChanges


class ActionTagsFactory(DjangoModelFactory):
    class Meta:
        model = ActionTags


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote


class QuoteSuggestionChangesFactory(DjangoModelFactory):
    class Meta:
        model = QuoteSuggestionChanges


class QuoteSuggestionFactory(DjangoModelFactory):
    class Meta:
        model = QuoteSuggestion


class QuoteTagsFactory(DjangoModelFactory):
    class Meta:
        model = QuoteTags


def create_actions():
    dir_path = os.path.join(__location__, "..", "data")

    with open(
        os.path.join(dir_path, "actions_tags.json"),
        encoding="utf-8",
    ) as tags_file:
        tags = json.load(tags_file)
        for tag in tags:
            del tag["slug"]
            childrens = tag.pop("childrens")
            tag_obj = ActionTagsFactory(**tag)
            for children in childrens:
                del children["slug"]
                ActionTagsFactory(**children, parent=tag_obj)

    with open(
        os.path.join(dir_path, "actions.json"),
        encoding="utf-8",
    ) as actions_file:
        actions = json.load(actions_file)
        for action in actions:
            action_tags = action.pop("tags")
            date = datetime.strptime(action.pop("date"), "%d/%m/%Y").date()
            action_obj = ActionFactory(**{**action, "date": date})
            action_obj.tags.add(*action_tags)  # taggit needs a pk
            action_obj.save()


def create_quotes():
    dir_path = os.path.join(__location__, "..", "data")

    with open(
        os.path.join(dir_path, "quotes_tags.json"),
        encoding="utf-8",
    ) as tags_file:
        tags = json.load(tags_file)
        for tag in tags:
            del tag["slug"]
            childrens = tag.pop("childrens")
            tag_obj = QuoteTagsFactory(**tag)
            for children in childrens:
                del children["slug"]
                QuoteTagsFactory(**children, parent=tag_obj)

    with open(
        os.path.join(dir_path, "quotes.json"),
        encoding="utf-8",
    ) as quotes_file:
        quotes = json.load(quotes_file)
        for quote in quotes:
            quote_tags = quote.pop("tags")
            date = datetime.strptime(quote.pop("date"), "%d/%m/%Y").date()
            quotes_obj = QuoteFactory(**{**quote, "date": date})
            quotes_obj.tags.add(*quote_tags)  # taggit needs a pk
            quotes_obj.save()


# https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-don-t-use-transactional-or-live-server
@pytest.fixture(scope="session")
def django_db_setup(
    django_db_setup,  # pylint: disable=unused-argument
    django_db_blocker,
):
    with django_db_blocker.unblock():
        create_actions()
        create_quotes()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def action_tag():
    return ActionTagsFactory(name="Test", slug="test")


@pytest.fixture
def quote_tag():
    return QuoteTagsFactory(name="Test", slug="test")


@pytest.fixture
def user_email():
    return "test@test.com"


@pytest.fixture
def action_fields():
    return [
        "id",
        "tags",
        "description",
        "source",
        "date",
        "date_is_estimated",
        "additional_infos",
    ]


@pytest.fixture
def action_data():
    return {
        "id": 1000,
        "date": "03/07/2020",
        "description": (
            "Veto ao uso obrigatório de máscaras, em meio a pandemia de coronavírus."
        ),
        "source": (
            "https://g1.globo.com/politica/noticia/2020/07/03/bolsonaro-sanciona-com-vetos-lei-"
            "que-obriga-uso-de-mascaras-em-locais-publicos-pelo-pais.ghtml"
        ),
        "date_is_estimated": False,
        "additional_infos": (
            "O presidente vetou a obrigatoriedade de máscaras em órgãos e entidades públicas, "
            "estabelecimentos comerciais, industriais, templos religiosos e demais locais "
            "fechados em que haja reunião de pessoas."
        ),
    }


@pytest.fixture
def action_tags():
    return ["Anticiência", "Coronavírus", "Ministério da Saúde"]


@pytest.fixture
def action_suggest_data(action_data, action_tags, user_email):
    del action_data["id"]
    action_data["user_email"] = user_email
    action_data["tags"] = action_tags
    return action_data


@pytest.fixture
def action(action_data, action_tags):
    obj = ActionFactory(
        **{
            **action_data,
            "date": datetime.strptime(action_data["date"], "%d/%m/%Y").date(),
        }
    )
    obj.tags.add(*action_tags)
    obj.save()
    return obj


@pytest.fixture
def action_suggestion_change(action, action_data, action_tags, user_email):
    action_data["user_email"] = user_email
    obj = ActionSuggestionChangesFactory(
        **{
            **action_data,
            "date": datetime.strptime(action_data["date"], "%d/%m/%Y").date(),
            "original_action": action,
            "justification": "test",
        }
    )
    obj.tags.add(*action_tags)
    obj.save()
    return obj


@pytest.fixture
def action_suggestion(action_data, action_tags):
    action_data["user_email"] = user_email
    obj = ActionSuggestionFactory(
        **{
            **action_data,
            "date": datetime.strptime(action_data["date"], "%d/%m/%Y").date(),
        }
    )
    obj.tags.add(*action_tags)
    obj.save()
    return obj


@pytest.fixture
def quote_fields():
    return [
        "id",
        "tags",
        "description",
        "source",
        "is_fake_news",
        "fake_news_source",
        "date",
        "date_is_estimated",
        "additional_infos",
    ]


@pytest.fixture
def quote_data():
    return {
        "id": 1000,
        "date": "10/11/2020",
        "description": "Morte, invalidez, anomalia. Esta é a vacina que o Doria queria [...]",
        "source": (
            "https://g1.globo.com/politica/noticia/2020/11/10/mais-uma-que-jair-bolsonaro-"
            "ganha-diz-o-presidente-ao-comentar-suspensao-de-testes-da-vacina-coronavac.ghtml"
        ),
        "is_fake_news": True,
        "fake_news_source": (
            "https://politica.estadao.com.br/blogs/estadao-verifica/coronavac-teve-apenas"
            "-efeitos-colaterais-leves-e-falso-que-voluntarios-tenham-morrido/"
        ),
        "date_is_estimated": False,
        "additional_infos": (
            "Sem apresentar provas, Bolsonaro conclui efeitos "
            "adversos da vacina coronaVac."
        ),
    }


@pytest.fixture
def quote_tags():
    return ["Fake news", "Coronavírus"]


@pytest.fixture
def quote_suggest_data(quote_data, quote_tags, user_email):
    del quote_data["id"]
    quote_data["user_email"] = user_email
    quote_data["tags"] = quote_tags
    return quote_data


@pytest.fixture
def quote(quote_data, quote_tags):
    obj = QuoteFactory(
        **{
            **quote_data,
            "date": datetime.strptime(quote_data["date"], "%d/%m/%Y").date(),
        }
    )
    obj.tags.add(*quote_tags)
    obj.save()
    return obj


@pytest.fixture
def quote_suggestion_change(quote, quote_data, quote_tags, user_email):
    quote_data["user_email"] = user_email
    obj = QuoteSuggestionChangesFactory(
        **{
            **quote_data,
            "date": datetime.strptime(quote_data["date"], "%d/%m/%Y").date(),
            "original_quote": quote,
            "justification": "test",
        }
    )
    obj.tags.add(*quote_tags)
    obj.save()
    return obj


@pytest.fixture
def quote_suggestion(quote_data, quote_tags):
    quote_data["user_email"] = user_email
    obj = QuoteSuggestionFactory(
        **{
            **quote_data,
            "date": datetime.strptime(quote_data["date"], "%d/%m/%Y").date(),
        }
    )
    obj.tags.add(*quote_tags)
    obj.save()
    return obj


@pytest.fixture
def entities(action, quote):
    return action, quote


@pytest.fixture
def entities_suggestions_change(action_suggestion_change, quote_suggestion_change):
    return action_suggestion_change, quote_suggestion_change


@pytest.fixture
def entities_suggestions(action_suggestion, quote_suggestion):
    return action_suggestion, quote_suggestion


@pytest.fixture
def action_base_url():
    return f"/{API_BASE_URL}" + "actions"


@pytest.fixture
def quote_base_url():
    return f"/{API_BASE_URL}" + "quotes"


@pytest.fixture
def base_urls(action_base_url, quote_base_url):
    return action_base_url, quote_base_url


@pytest.fixture
def entities_suggest_data(action_suggest_data, quote_suggest_data):
    return action_suggest_data, quote_suggest_data


@pytest.fixture
def fields(action_fields, quote_fields):
    return action_fields, quote_fields


@pytest.fixture
def tags(action_tag, quote_tag):
    return action_tag, quote_tag


@pytest.fixture
def wsgi_request():
    return WSGIRequest(
        {
            "SERVER_NAME": "127.0.0.1",
            "SERVER_PORT": 443,
            "REQUEST_METHOD": "GET",
            "wsgi.input": None,
            "wsgi.url_scheme": "http",
        }
    )


@pytest.fixture
def generic_post_request():
    request = HttpRequest()
    request.method = "POST"
    request.META = {"SERVER_NAME": "127.0.0.1", "SERVER_PORT": 443}
    return request


@pytest.fixture
def accept_suggestion_request(generic_post_request):
    generic_post_request.POST = {"accept-suggestion": True}
    return generic_post_request


@pytest.fixture
def decline_suggestion_request(generic_post_request):
    generic_post_request.POST = {"decline-suggestion": True}
    return generic_post_request
