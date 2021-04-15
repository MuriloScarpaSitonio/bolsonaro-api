from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest


def get_generic_request() -> HttpRequest:
    request = HttpRequest()
    request.method = "GET"
    request.META = {"SERVER_NAME": settings.ALLOWED_HOSTS[0], "SERVER_PORT": 443}
    return request


def get_post_request(post_params: Dict[str, Any]) -> HttpRequest:
    request = get_generic_request()
    request.method = "POST"
    request.POST = post_params
    return request
