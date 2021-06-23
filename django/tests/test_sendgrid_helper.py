import pytest
from python_http_client.exceptions import HTTPError

from django.conf import settings

from core.helpers.sendgrid_helper import (
    send_suggestion_accepted_email,
    send_suggestion_declined_email,
    send_suggestion_received_email,
)


pytestmark = pytest.mark.django_db


def test_send_suggestion_accepted_email(mocker, entities, user_email, wsgi_request):
    # GIVEN
    mocked_send_mail = mocker.patch("core.helpers.sendgrid_helper.send_mail")

    # WHEN
    for entity in entities:
        entity_name = entity.__class__.__name__.lower()
        send_suggestion_accepted_email(
            request=wsgi_request,
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
            f"http://127.0.0.1:443/{entity_name}s/{entity.id}/"
            in mocked_send_mail.call_args[1]["html_message"]
        )


def test_should_log_error_if_excpetion_suggestion_accepted(
    mocker, entities, user_email, wsgi_request
):
    # GIVEN
    mocked_logger = mocker.patch("core.helpers.sendgrid_helper.logger")
    mocker.patch(
        "core.helpers.sendgrid_helper.send_mail",
        side_effect=HTTPError(400, "reason", "body", "headers"),
    )

    for entity in entities:
        # WHEN
        send_suggestion_accepted_email(
            request=wsgi_request,
            user_email=user_email,
            obj=entity,
        )

        # THEN
        assert mocked_logger.error.call_args[0][0] == (
            "Nao foi possivel enviar o e-mail de sugestao aceita para %s. "
            "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
        )


def test_send_suggestion_declined_email_with_feedback(mocker, user_email, wsgi_request):
    # GIVEN
    mocked_send_mail = mocker.patch("core.helpers.sendgrid_helper.send_mail")
    feedback = "Feedback teste"

    # WHEN
    send_suggestion_declined_email(
        request=wsgi_request,
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


def test_send_suggestion_declined_email_without_feedback(
    mocker, user_email, wsgi_request
):
    # GIVEN
    mocked_send_mail = mocker.patch("core.helpers.sendgrid_helper.send_mail")

    # WHEN
    send_suggestion_declined_email(
        request=wsgi_request,
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


def test_should_log_error_if_excpetion_suggestion_declined(
    mocker, user_email, wsgi_request
):
    # GIVEN
    mocked_logger = mocker.patch("core.helpers.sendgrid_helper.logger")
    mocker.patch(
        "core.helpers.sendgrid_helper.send_mail",
        side_effect=HTTPError(400, "reason", "body", "headers"),
    )

    # WHEN
    send_suggestion_declined_email(
        request=wsgi_request,
        user_email=user_email,
        feedback=None,
    )

    # THEN
    assert mocked_logger.error.call_args[0][0] == (
        "Nao foi possivel enviar o e-mail de sugestao rejeitada para %s. "
        "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
    )


def test_send_suggestion_received_email_entity_suggestion_change(
    mocker, entities_suggestions_change, user_email, wsgi_request
):
    # GIVEN
    mocked_send_mail = mocker.patch("core.helpers.sendgrid_helper.send_mail")
    wsgi_request.data = {"user_email": user_email}

    # WHEN
    for entity in entities_suggestions_change:
        entity_name = entity.__class__.__name__.lower().split("suggestionchanges")[0]
        original_id = getattr(entity, f"original_{entity_name}").id
        send_suggestion_received_email(request=wsgi_request, obj=entity)

        # THEN
        assert mocked_send_mail.call_args[1]["subject"] == "Sugestão em análise :)"
        assert (
            mocked_send_mail.call_args[1]["from_email"]
            == f"Bolsonaro API <{settings.EMAIL_HOST_USER}>"
        )
        assert mocked_send_mail.call_args[1]["recipient_list"] == [user_email]
        assert (
            f"http://127.0.0.1:443/{entity_name}s/{original_id}/"
            in mocked_send_mail.call_args[1]["html_message"]
        )


def test_send_suggestion_received_email_entity_suggestion(
    mocker, entities_suggestions, user_email, wsgi_request
):
    # GIVEN
    mocked_send_mail = mocker.patch("core.helpers.sendgrid_helper.send_mail")
    wsgi_request.data = {"user_email": user_email}

    # WHEN
    for entity in entities_suggestions:
        entity_name = (
            "ação"
            if entity.__class__.__name__.lower().split("suggestion")[0] == "action"
            else "declaração"
        )
        send_suggestion_received_email(request=wsgi_request, obj=entity)

        # THEN
        assert mocked_send_mail.call_args[1]["subject"] == "Sugestão em análise :)"
        assert (
            mocked_send_mail.call_args[1]["from_email"]
            == f"Bolsonaro API <{settings.EMAIL_HOST_USER}>"
        )
        assert mocked_send_mail.call_args[1]["recipient_list"] == [user_email]
        assert (
            f"Analisaremos assim que possível a sugestão da {entity_name}"
            in mocked_send_mail.call_args[1]["html_message"]
        )
        assert entity.description in mocked_send_mail.call_args[1]["html_message"]


def test_should_log_error_if_excpetion_suggestion_received(
    mocker, entities_suggestions, user_email, wsgi_request
):
    # GIVEN
    mocked_logger = mocker.patch("core.helpers.sendgrid_helper.logger")
    mocker.patch(
        "core.helpers.sendgrid_helper.send_mail",
        side_effect=HTTPError(400, "reason", "body", "headers"),
    )
    wsgi_request.data = {"user_email": user_email}

    # WHEN
    for entity in entities_suggestions:
        send_suggestion_received_email(request=wsgi_request, obj=entity)

        # THEN
        assert mocked_logger.error.call_args[0][0] == (
            "Nao foi possivel enviar o e-mail de sugestao recebida para %s. "
            "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
        )
