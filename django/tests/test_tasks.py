import pytest

from actions.tasks import post_action_tweet
from quotes.tasks import post_quote_tweet

pytestmark = pytest.mark.django_db


def test_post_action_tweet(mocker, action_data):
    # GIVEN
    mocked_api = mocker.patch("helpers.tasks_helper.TwitterApi")
    mocker.patch("helpers.tasks_helper._get_random_entity", return_value=action_data)

    # WHEN
    post_action_tweet()

    # THEN
    assert mocked_api.call_count == 1
    assert mocked_api.return_value.PostUpdate.call_args[1]["status"] == (
        f"{action_data['description']}\n\n"
        f"Mais informações: http://bolsonaro-api.herokuapp.com/actions/{action_data['id']}/"
    )


def test_post_quote_tweet(mocker, quote_data):
    # GIVEN
    mocked_api = mocker.patch("helpers.tasks_helper.TwitterApi")
    mocker.patch("helpers.tasks_helper._get_random_entity", return_value=quote_data)
    description = f'"{quote_data["description"]}"'

    # WHEN
    post_quote_tweet()

    # THEN
    assert mocked_api.call_count == 1
    assert mocked_api.return_value.PostUpdate.call_args[1]["status"] == (
        f"{description}\n\n"
        f"Mais informações: http://bolsonaro-api.herokuapp.com/quotes/{quote_data['id']}/"
    )
