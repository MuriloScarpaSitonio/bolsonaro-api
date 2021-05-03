import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "text", ["eunaoexisto", "eu nao existo", "nãooooooooooo", "eu não existo"]
)
def test_get_all_by_non_existing_text(api_client, base_urls, text):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + f"?description={text}"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data == []


@pytest.mark.parametrize("text", ["ção", "crimes ambientais", "ão d"])
def test_get_all_entities_by_existing_text(api_client, base_urls, text, fields):
    # GIVEN
    for base_url, field in zip(base_urls, fields):

        # WHEN
        url = base_url + f"?description={text}"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data
        assert all(
            all(key in field for key in entity.keys()) for entity in response.data
        )
        assert all(text in entity["description"] for entity in response.data)


def test_get_entities_with_pagination(api_client, base_urls, fields):

    # GIVEN
    for base_url, field in zip(base_urls, fields):
        text = "a"

        # WHEN
        url = base_url + f"?description={text}&page=1"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data
        assert sorted(list(response.data.keys())) == ["hasMore", "results"]
        assert all(
            all(key in field for key in entity.keys())
            for entity in response.data["results"]
        )
        assert len(response.data["results"]) == 10  # page_size = 10
        assert all(text in entity["description"] for entity in response.data["results"])
        assert response.data["hasMore"]


def test_get_all_tags_with_pagination(api_client, base_urls):

    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "/tags?page=1"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data
        assert sorted(list(response.data.keys())) == ["hasMore", "results"]
        assert all(
            all(key in ("name", "slug") for key in tag.keys())
            for tag in response.data["results"]
        )
        assert len(response.data["results"]) == 10  # page_size = 10
        assert response.data["hasMore"]


def test_get_random(api_client, base_urls, fields):
    # GIVEN
    for base_url, field in zip(base_urls, fields):

        # WHEN
        url = base_url + "/random"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data
        assert isinstance(response.data, dict)
        assert all(key in field for key in response.data.keys())


def test_get_by_existing_id(api_client, base_urls, fields):
    # GIVEN
    for base_url, field in zip(base_urls, fields):

        # WHEN
        url = base_url + "/5"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.data
        assert isinstance(response.data, dict)
        assert all(key in field for key in response.data.keys())


def test_get_by_non_existing_id(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "/0"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Não encontrado."}


def test_get_entities_without_tags_arg(api_client, base_urls, fields):
    # GIVEN
    for base_url, field in zip(base_urls, fields):

        # WHEN
        url = base_url + "?tags="
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert all(
            all(key in field for key in entity.keys()) for entity in response.data
        )


def test_get_all_actions_by_existing_tag(api_client, action_base_url, action_fields):
    # GIVEN

    # WHEN
    url = action_base_url + "?tags=coronavirus"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 10
    assert all(
        all(key in action_fields for key in action.keys()) for action in response.data
    )
    assert all("Coronavírus" in action["tags"] for action in response.data)


def test_get_all_actions_by_multiple_existing_tag(
    api_client,
    action_base_url,
    action_fields,
):
    # GIVEN

    # WHEN
    url = action_base_url + "?tags=coronavirus,ministerio-da-educacao"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 28
    assert all(
        all(key in action_fields for key in action.keys()) for action in response.data
    )
    assert all(
        "Coronavírus" in action["tags"] or "Ministério da Educação" in action["tags"]
        for action in response.data
    )


def test_get_all_actions_tags(api_client, action_base_url):
    # GIVEN

    # WHEN
    url = action_base_url + "/tags"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 31
    assert all(list(tag.keys()) == ["name", "slug"] for tag in response.data)


def test_get_all_actions_main_tags(api_client, action_base_url):
    # GIVEN

    # WHEN
    url = action_base_url + "/tags/main"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 23
    assert all(
        list(tag.keys()) == ["name", "slug", "childrens"] for tag in response.data
    )


def test_get_all_quotes_by_existing_tag(api_client, quote_base_url, quote_fields):
    # GIVEN

    # WHEN
    url = quote_base_url + "?tags=lgbt"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 8
    assert all(
        all(key in quote_fields for key in quote.keys()) for quote in response.data
    )
    assert all("LGBT" in quote["tags"] for quote in response.data)


def test_get_all_quotes_by_multiple_existing_tag(
    api_client,
    quote_base_url,
    quote_fields,
):
    # GIVEN

    # WHEN
    url = quote_base_url + "?tags=lgbt,dilma"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 11
    assert all(
        all(key in quote_fields for key in quote.keys()) for quote in response.data
    )
    assert all(
        "LGBT" in quote["tags"] or "Dilma" in quote["tags"] for quote in response.data
    )


def test_get_all_quotes_tags(api_client, quote_base_url):
    # GIVEN

    # WHEN
    url = quote_base_url + "/tags"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 30
    assert all(list(tag.keys()) == ["name", "slug"] for tag in response.data)


def test_get_all_quotes_main_tags(api_client, quote_base_url):
    # GIVEN

    # WHEN
    url = quote_base_url + "/tags/main"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 19
    assert all(
        list(tag.keys()) == ["name", "slug", "childrens"] for tag in response.data
    )


def test_should_raise_bad_request_if_non_existing_tag(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "?tags=do-not-exist"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["errorMessage"])
            == "A(s) seguinte(s) tag(s) não existe(m): do-not-exist."
        )


@pytest.mark.usefixtures("tags")
def test_should_raise_bad_request_if_non_existing_tag_and_existing(
    api_client,
    base_urls,
):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "?tags=do-not-exist,test"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert (
            str(response.data["errorMessage"])
            == "A(s) seguinte(s) tag(s) não existe(m): do-not-exist."
        )


def test_count_endpoint(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:
        expected = 140 if "actions" in base_url else 116

        # WHEN
        url = base_url + "/count"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.json()["total"] == expected


def test_should_get_tag_by_slug(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "/tags/corrupcao"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"name": "Corrupção", "slug": "corrupcao"}


def test_should_not_get_tag_if_no_existing_slug(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "/tags/do-not-exist"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Não encontrado."}


def test_should_filter_by_tags_if_slugs_with_space(api_client, base_urls):
    # GIVEN
    for base_url in base_urls:

        # WHEN
        url = base_url + "?tags=censura,     falta-de-decoro"
        response = api_client.get(url)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert all(
            "Censura" in entity["tags"] or "Falta de decoro" in entity["tags"]
            for entity in response.data
        )


def test_should_get_entities_with_children_tags(api_client, action_base_url):
    # GIVEN

    # WHEN
    url = action_base_url + "?tags=ministerio-da-saude"
    response = api_client.get(url)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert all(
        "Anvisa" in action["tags"] or "Ministério da Saúde" in action["tags"]
        for action in response.data
    )
