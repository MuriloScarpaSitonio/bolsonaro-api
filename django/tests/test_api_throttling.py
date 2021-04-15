from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS

from core.consts import API_BASE_URL


def test_throttle_limit(api_client):
    # GIVEN
    throttle_limit = 1000
    url = f"/{API_BASE_URL}"

    # WHEN
    for _ in range(throttle_limit):
        api_client.get(url)
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_429_TOO_MANY_REQUESTS
