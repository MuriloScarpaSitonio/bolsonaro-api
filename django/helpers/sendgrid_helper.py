import logging
from typing import Union

from python_http_client.exceptions import HTTPError

from actions.models import Action
from actions.serializers import ActionSuggestion, ActionSuggestionChanges
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from quotes.models import Quote
from quotes.serializers import QuoteSuggestion, QuoteSuggestionChanges

logger = logging.getLogger("db")


def send_suggestion_accepted_email(
    request: WSGIRequest, user_email: str, obj: Union[Action, Quote]
) -> None:
    """Função que envia email informando que a sugestão do usuário foi informada.

    Args:
        request (WSGIRequest): A requisição enviada pelo servidor.
        user_email (str): O e-mail do usuário.
        obj (Union[Action, Quote]): Objeto que representa a entidade aceita.
    """
    html_message = render_to_string(
        "suggestion_accepted_email_body.html",
        {
            "obj_id": obj.id,
            "obj_class_name": obj.__class__.__name__.lower(),
            "request": request,
        },
    )
    try:
        send_mail(
            subject="Sua sugestão foi aceita!",
            message=strip_tags(html_message),
            from_email=f"Bolsonaro API <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info("E-mail de sugestao aceita enviado com sucesso para %s", user_email)
    except HTTPError as error:
        # https://github.com/sendgrid/sendgrid-python/blob/main/use_cases/error_handling.md
        logger.error(
            (
                "Nao foi possivel enviar o e-mail de sugestao aceita para %s. "
                "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
            ),
            user_email,
            error.status_code,
            str(error),
            error.body,
            error.reason,
            error.headers,
        )


def send_suggestion_declined_email(
    request: WSGIRequest, user_email: str, feedback: Union[str, None]
) -> None:
    """Função que envia email informando que a sugestão do usuário foi aceita.

    Args:
        request (WSGIRequest): A requisição enviada pelo servidor.
        user_email (str): O e-mail do usuário.
        feedback (Union[str, None]): O feedback do admin sobre a sugestão do usuário.
    """
    html_message = render_to_string(
        "suggestion_declined_email_body.html",
        {"feedback": feedback, "request": request},
    )
    try:
        send_mail(
            subject="Sua sugestão foi rejeitada",
            message=strip_tags(html_message),
            from_email=f"Bolsonaro API <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(
            "E-mail de sugestao rejeitada enviado com sucesso para %s", user_email
        )
    except HTTPError as error:
        logger.error(
            (
                "Nao foi possivel enviar o e-mail de sugestao rejeitada para %s. "
                "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
            ),
            user_email,
            error.status_code,
            str(error),
            error.body,
            error.reason,
            error.headers,
        )


def send_suggestion_received_email(
    request: WSGIRequest,
    obj: Union[
        ActionSuggestion,
        ActionSuggestionChanges,
        QuoteSuggestion,
        QuoteSuggestionChanges,
    ],
) -> None:
    """Função que envia email confirmado o recebimento da sugestão do usuário.

    Args:
        request (WSGIRequest): A requisição enviada pelo servidor.
        obj (Union[ActionSuggestion,
                   ActionSuggestionChanges,
                   QuoteSuggestion,
                   QuoteSuggestionChanges]
            ): Objeto que representa uma sugestão de entidade.
    """
    html_message = render_to_string(
        "suggestion_received_email_body.html",
        {
            "request": request,
            "obj": obj,
            "obj_class_name": obj.__class__.__name__.lower(),
        },
    )

    user_email = request.data.get("user_email")
    try:
        send_mail(
            subject="Sugestão em análise :)",
            message=strip_tags(html_message),
            from_email=f"Bolsonaro API <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(
            "E-mail de sugestao recebida enviado com sucesso para %s", user_email
        )
    except HTTPError as error:
        logger.error(
            (
                "Nao foi possivel enviar o e-mail de sugestao recebida para %s. "
                "Code: %s | Error: %s | Body: %s | Reason: %s | Headers: %s"
            ),
            user_email,
            error.status_code,
            str(error),
            error.body,
            error.reason,
            error.headers,
        )
