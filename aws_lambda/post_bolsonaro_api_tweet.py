from argparse import ArgumentParser
import logging
import os

import requests
from requests.exceptions import HTTPError
from twitter import Api as TwitterApi
from twitter.error import TwitterError


logger = logging.getLogger()
logger.setLevel(getattr(logging, os.getenv("log_level", "INFO")))


def get_base_api_url() -> str:
    base_api_url = os.getenv("BOLSONARO_API_BASE_URL")
    if base_api_url is None:
        raise RuntimeError("BOLSONARO_API_BASE_URL is not set")
    return base_api_url


def get_entity_infos(entity_name: str, base_api_url: str):
    response = requests.get(f"{base_api_url}/{entity_name}/random")
    response.raise_for_status()
    return response.json()


def post_bolsonaro_api_tweet(entity_name: str) -> None:
    logger.info("Posting %s tweet...", entity_name)

    api = TwitterApi(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET_KEY"),
        access_token_key=os.getenv("TWITTER_API_TOKEN"),
        access_token_secret=os.getenv("TWITTER_API_SECRET_TOKEN"),
    )

    try:
        base_api_url = get_base_api_url()
        infos = get_entity_infos(entity_name=entity_name, base_api_url=base_api_url)
    except (RuntimeError, HTTPError) as error:
        logger.critical(
            "Unable to get infos from the given entity. Error: %s", error.args[0]
        )
        raise error

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
        raise error


if __name__ == "__main__":
    parser = ArgumentParser(description="Post Bolsonaro tweet")
    parser.add_argument(
        "entity_name",
        help="Which kind of tweet we are going to post",
        choices=("actions", "quotes"),
    )
    post_bolsonaro_api_tweet(entity_name=vars(parser.parse_args())["entity_name"])
