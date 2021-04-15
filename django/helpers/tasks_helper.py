import logging
from typing import Any, Dict, Union

from twitter import Api as TwitterApi
from twitter.error import TwitterError

from actions.views import ActionViewSet
from django.conf import settings
from quotes.views import QuoteViewSet

from .utils import get_generic_request

logger = logging.getLogger("db")


def _get_random_entity(
    view_set_obj: Union[ActionViewSet, QuoteViewSet]
) -> Dict[str, Any]:
    return view_set_obj.random(get_generic_request()).data


def post_entity_tweet(view_set_obj: Union[ActionViewSet, QuoteViewSet]) -> None:
    """Função que posta um tweet de uma entidade (ação ou declaração).

    Args:
        view_set_obj (Union[ActionViewSet, QuoteViewSet]): O ViewSet da entidade.
    """
    api = TwitterApi(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET_KEY,
        access_token_key=settings.TWITTER_API_TOKEN,
        access_token_secret=settings.TWITTER_API_SECRET_TOKEN,
    )

    entity_name = view_set_obj.__class__.__name__.split("ViewSet")[0].lower()
    infos = _get_random_entity(view_set_obj=view_set_obj)
    if isinstance(view_set_obj, QuoteViewSet):
        infos["description"] = f'"{infos["description"]}"'

    try:
        api.PostUpdate(
            status=(
                f"{infos['description']}\n\nMais informações: "
                f"http://bolsonaro-api.herokuapp.com/{entity_name}s/{infos['id']}/"
            )
        )
        logger.info(
            "%s tweet postado com sucesso. ID da entidade: %s", entity_name, infos["id"]
        )
    except TwitterError as error:
        logger.error("Erro ao postar no twitter: %s", error.message)
