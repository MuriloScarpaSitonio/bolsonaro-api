import pytest
from twitter.error import TwitterError

from ..post_bolsonaro_api_tweet import post_bolsonaro_api_tweet


def test_should_post_actions_tweet(
    mocker, requests_mock, bolsonaro_api_url, action_data
):
    # GIVEN
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(
        f"{bolsonaro_api_url}/actions/random", json=action_data, status_code=200
    )

    # WHEN
    post_bolsonaro_api_tweet(entity_name="actions")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 1
    assert mocked_twitter_api.return_value.PostUpdate.call_args[1]["status"] == (
        f"{action_data['description']}\n\n"
        f"Mais informações: {bolsonaro_api_url}/actions/{action_data['id']}/"
    )


def test_should_post_quotes_tweet(mocker, requests_mock, bolsonaro_api_url, quote_data):
    # GIVEN
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(
        f"{bolsonaro_api_url}/quotes/random", json=quote_data, status_code=200
    )
    description = f'"{quote_data["description"]}"'

    # WHEN
    post_bolsonaro_api_tweet(entity_name="quotes")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 1
    assert mocked_twitter_api.return_value.PostUpdate.call_args[1]["status"] == (
        f"{description}\n\n"
        f"Mais informações: {bolsonaro_api_url}/quotes/{quote_data['id']}/"
    )


def test_should_not_post_actions_tweet_if_bolsonaro_api_raises_error(
    mocker, requests_mock, bolsonaro_api_url
):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(f"{bolsonaro_api_url}/actions/random", status_code=500)

    # WHEN
    post_bolsonaro_api_tweet(entity_name="actions")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 0
    assert mocked_logger.critical.call_args[0] == (
        "Unable to get infos from the given entity. Error: %s",
        f"500 Server Error: None for url: {bolsonaro_api_url}/actions/random",
    )


def test_should_not_post_quotes_tweet_if_bolsonaro_api_raises_error(
    mocker, requests_mock, bolsonaro_api_url
):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(f"{bolsonaro_api_url}/quotes/random", status_code=500)

    # WHEN
    post_bolsonaro_api_tweet(entity_name="quotes")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 0
    assert mocked_logger.critical.call_args[0] == (
        "Unable to get infos from the given entity. Error: %s",
        f"500 Server Error: None for url: {bolsonaro_api_url}/quotes/random",
    )


def test_should_not_post_actions_tweet_if_twitter_api_raises_error(
    mocker, requests_mock, bolsonaro_api_url, action_data
):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(
        f"{bolsonaro_api_url}/actions/random", json=action_data, status_code=200
    )
    mocked_twitter_api.return_value.PostUpdate.side_effect = TwitterError(
        "Error: Timeout"
    )

    # WHEN
    post_bolsonaro_api_tweet(entity_name="actions")

    # THEN
    assert mocked_logger.critical.call_args[0] == (
        "Error posting tweet: %s",
        "Error: Timeout",
    )


def test_should_not_post_quotes_tweet_if_twitter_api_raises_error(
    mocker, requests_mock, bolsonaro_api_url, action_data
):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")
    requests_mock.get(
        f"{bolsonaro_api_url}/quotes/random", json=action_data, status_code=200
    )
    mocked_twitter_api.return_value.PostUpdate.side_effect = TwitterError(
        "Error: Timeout"
    )

    # WHEN
    post_bolsonaro_api_tweet(entity_name="quotes")

    # THEN
    assert mocked_logger.critical.call_args[0] == (
        "Error posting tweet: %s",
        "Error: Timeout",
    )


@pytest.mark.noenvvars
def test_should_not_post_actions_tweet_if_bolsonaro_api_url_env_var_is_not_set(mocker):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")

    # WHEN
    post_bolsonaro_api_tweet(entity_name="actions")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 0
    assert mocked_logger.critical.call_args[0] == (
        "Unable to get infos from the given entity. Error: %s",
        "BOLSONARO_API_BASE_URL env variable is not set",
    )


@pytest.mark.noenvvars
def test_should_not_post_quotes_tweet_if_bolsonaro_api_url_env_var_is_not_set(mocker):
    # GIVEN
    mocked_logger = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.logger")
    mocked_twitter_api = mocker.patch("aws_lambda.post_bolsonaro_api_tweet.TwitterApi")

    # WHEN
    post_bolsonaro_api_tweet(entity_name="quotes")

    # THEN
    assert mocked_twitter_api.return_value.PostUpdate.call_count == 0
    assert mocked_logger.critical.call_args[0] == (
        "Unable to get infos from the given entity. Error: %s",
        "BOLSONARO_API_BASE_URL env variable is not set",
    )
