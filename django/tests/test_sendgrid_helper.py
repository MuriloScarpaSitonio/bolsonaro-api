import pytest

from django.conf import settings
from helpers.sendgrid_helper import (  # send_suggestion_received_email,
    send_suggestion_accepted_email,
    send_suggestion_declined_email,
)
from helpers.utils import get_generic_request

# from python_http_client.exceptions import HTTPError


pytestmark = pytest.mark.django_db


def test_send_suggestion_accepted_email(mocker, entities, user_email):
    # GIVEN
    mocked_send_mail = mocker.patch("helpers.sendgrid_helper.send_mail")

    # WHEN
    for entity in entities:
        entity_name = entity.__class__.__name__.lower()
        send_suggestion_accepted_email(
            request=get_generic_request(),
            user_email=user_email,
            obj=entity,
        )

        # THEN
        assert mocked_send_mail.call_args[1]["subject"] == "Sua sugestão foi aceita!"
        assert (
            mocked_send_mail.call_args[1]["from_email"]
            == f"Bolsonaro API <{settings.EMAIL_HOST_USER}>"
        )
        assert mocked_send_mail.call_args[1]["recipient_list"] == [user_email]
        assert (
            f"http://{settings.ALLOWED_HOSTS[0]}:443/{entity_name}s/{entity.id}/"
            in mocked_send_mail.call_args[1]["html_message"]
        )


# pylint: disable=pointless-string-statement
"""
def test_send_suggestion_with_exception(mocker, entities, user_email):
    def test(*args, **kwargs):
        raise HTTPError(400, "reason", "body", "headers")

    mocked_logger = mocker.patch("helpers.sendgrid_helper.logger")
    mocker.patch("helpers.sendgrid_helper.render_to_string", test)

    # WHEN
    for entity in entities:
        with pytest.raises(HTTPError):
            send_suggestion_accepted_email(
                request=get_generic_request(),
                user_email=user_email,
                obj=entity,
            )

    # THEN
    assert mocked_logger.call_count == 2"""


def test_send_suggestion_declined_email_with_feedback(mocker, user_email):
    # GIVEN
    mocked_send_mail = mocker.patch("helpers.sendgrid_helper.send_mail")
    feedback = "Feedback teste"

    # WHEN
    send_suggestion_declined_email(
        request=get_generic_request(),
        user_email=user_email,
        feedback=feedback,
    )

    # THEN
    assert mocked_send_mail.call_count == 1
    assert mocked_send_mail.call_args[1]["subject"] == "Sua sugestão foi rejeitada"
    assert (
        mocked_send_mail.call_args[1]["from_email"]
        == f"Bolsonaro API <{settings.EMAIL_HOST_USER}>"
    )
    assert mocked_send_mail.call_args[1]["recipient_list"] == [user_email]
    assert (
        "Confira mais detalhes, dos motivos da rejeição, "
        f'enviados pela equipe que administra o site: "{feedback}"'
    ) not in mocked_send_mail.call_args[1]["html_message"]


def test_send_suggestion_declined_email_without_feedback(mocker, user_email):
    # GIVEN
    mocked_send_mail = mocker.patch("helpers.sendgrid_helper.send_mail")

    # WHEN
    send_suggestion_declined_email(
        request=get_generic_request(),
        user_email=user_email,
        feedback=None,
    )

    # THEN
    assert mocked_send_mail.call_count == 1
    assert mocked_send_mail.call_args[1]["subject"] == "Sua sugestão foi rejeitada"
    assert (
        mocked_send_mail.call_args[1]["from_email"]
        == f"Bolsonaro API <{settings.EMAIL_HOST_USER}>"
    )
    assert mocked_send_mail.call_args[1]["recipient_list"] == [user_email]
    assert (
        "Confira mais detalhes, dos motivos da rejeição, "
        "enviados pela equipe que administra o site:"
    ) not in mocked_send_mail.call_args[1]["html_message"]


# pylint: disable=pointless-string-statement
"""
def test_send_suggestion_declined_with_exception(mocker, user_email):
    # GIVEN
    def test(*args, **kwargs):
        raise HTTPError(400, "reason", "body", "headers")

    mocked_logger = mocker.patch("helpers.sendgrid_helper.logger")
    mocker.patch("helpers.sendgrid_helper.render_to_string", test)

    # WHEN
    with pytest.raises(HTTPError):
        send_suggestion_declined_email(
            request=get_generic_request(),
            user_email=user_email,
            feedback=None,
        )

    # THEN
    assert mocked_logger.call_count == 1
"""
