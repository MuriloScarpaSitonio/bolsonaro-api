import logging
from os import getenv
from typing import Dict, List, Union

import requests
from requests.exceptions import HTTPError
from twitter import Api as TwitterApi
from twitter.error import TwitterError


logger = logging.getLogger()
logger.setLevel(getattr(logging, getenv("LOG_LEVEL", "INFO")))


def get_base_api_url() -> str:
    base_api_url = getenv("BOLSONARO_API_BASE_URL")
    if base_api_url in (None, ""):
        raise RuntimeError("BOLSONARO_API_BASE_URL env variable is not set")
    return base_api_url  # type: ignore


def get_entity_infos(
    entity_name: str, base_api_url: str
) -> Dict[str, Union[bool, int, str, List[str]]]:
    response = requests.get(f"{base_api_url}/{entity_name}/random")
    response.raise_for_status()
    return response.json()


def post_bolsonaro_api_tweet(entity_name: str) -> None:
    logger.info("Posting %s tweet...", entity_name)

    api = TwitterApi(
        consumer_key=getenv("TWITTER_API_KEY"),
        consumer_secret=getenv("TWITTER_API_SECRET_KEY"),
        access_token_key=getenv("TWITTER_API_TOKEN"),
        access_token_secret=getenv("TWITTER_API_SECRET_TOKEN"),
    )

    try:
        base_api_url = get_base_api_url()
        infos = get_entity_infos(entity_name=entity_name, base_api_url=base_api_url)
    except (RuntimeError, HTTPError) as error:
        logger.critical(
            "Unable to get infos from the given entity. Error: %s", error.args[0]
        )
        return

    if entity_name == "quotes":
        infos["description"] = f'"{infos["description"]}"'

    try:
        api.PostUpdate(
            status=(
                f"{infos['description']}\n\nMais informações: "
                f"{base_api_url}/{entity_name}/{infos['id']}/"
            )
        )
        logger.info("Successfully posted tweet. Entity's ID: %s", infos["id"])
    except TwitterError as error:
        logger.critical("Error posting tweet: %s", error.message)


def lambda_handler(event, context):  # pragma: no cover pylint: disable=unused-argument
    logger.info("Received event: %s", event)
    post_bolsonaro_api_tweet(entity_name=event["entity_name"])
