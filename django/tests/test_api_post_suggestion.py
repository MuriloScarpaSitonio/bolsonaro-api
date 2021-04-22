import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from core.consts import API_BASE_URL
from django.test import override_settings
from django.conf import settings

pytestmark = pytest.mark.django_db


def test_suggest_without_captcha(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


def test_suggest_with_wrong_captcha(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert (
            str(response.data["recaptcha"][0])
            == "Error verifying reCAPTCHA, please try again."
        )
        assert response.data["recaptcha"][0].code == "captcha_invalid"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert list(response.data.keys()) == ["message"]
        assert (
            response.data["message"]
            == "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
        )


@override_settings(DRF_RECAPTCHA_TESTING=True)
@pytest.mark.parametrize(
    "fields",
    [
        ("date_is_estimated",),
        ("additional_infos",),
        ("date_is_estimated", "additional_infos"),
    ],
)
def test_suggest_without_non_required_field(
    api_client,
    base_urls,
    entities_suggest_data,
    fields,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["recaptcha"] = "test"
        for field in fields:
            del entity_suggest_data[field]
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert list(response.data.keys()) == ["message"]
        assert (
            response.data["message"]
            == "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
        )


@pytest.mark.parametrize(
    "fields",
    [
        ("date_is_estimated",),
        ("additional_infos",),
        ("date_is_estimated", "additional_infos"),
    ],
)
def test_suggest_without_non_required_field_without_recaptcha(
    api_client,
    base_urls,
    entities_suggest_data,
    fields,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        for field in fields:
            del entity_suggest_data[field]
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


@pytest.mark.parametrize(
    "field", ["user_email", "tags", "date", "description", "source"]
)
def test_suggest_without_fields(
    api_client,
    base_urls,
    entities_suggest_data,
    field,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        del entity_suggest_data[field]
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert set(response.data.keys()) == set([field, "recaptcha"])
        assert str(response.data[field][0]) == "Este campo é obrigatório."
        assert response.data[field][0].code == "required"
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_with_non_existing_tag(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["tags"].append("Eu não existo")
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["tags"]
        assert str(response.data["tags"][0]) == (
            "A(s) tag(s) 'Eu não existo' "
            "não consta(m) na nossa base e por isso é(são) considerada(s) inválida(s). "
            "Se você pensa que ela(s) é(são) imprescindível(is) "
            f"contate-nos por e-mail ({settings.EMAIL_HOST_USER})."
        )
        assert response.data["tags"][0].code == "invalid"


def test_suggest_with_non_existing_tag_without_recaptcha(
    api_client,
    base_urls,
    entities_suggest_data,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["tags"].append("Eu não existo")
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_with_multiple_non_existing_tag(
    api_client,
    base_urls,
    entities_suggest_data,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["tags"].extend(["Eu não existo", "Eu também não", "Nem eu"])
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["tags"]
        assert str(response.data["tags"][0]) == (
            "A(s) tag(s) 'Eu não existo', 'Eu também não' e 'Nem eu' "
            "não consta(m) na nossa base e por isso é(são) considerada(s) inválida(s). "
            "Se você pensa que ela(s) é(são) imprescindível(is) "
            f"contate-nos por e-mail ({settings.EMAIL_HOST_USER})."
        )
        assert response.data["tags"][0].code == "invalid"


def test_suggest_with_multiple_non_existing_tag_without_recaptcha(
    api_client,
    base_urls,
    entities_suggest_data,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["tags"].extend(["Eu não existo", "Eu também não", "Nem eu"])
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


def test_suggest_with_wrong_date_format(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["date"] = "11/20/2020"
        response = api_client.post(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert set(response.data.keys()) == set(["date", "recaptcha"])
        assert (
            str(response.data["date"][0])
            == "Formato inválido para data. Use um dos formatos a seguir: DD/MM/YYYY."
        )
        assert response.data["date"][0].code == "invalid"
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_change_without_original_id(
    api_client,
    base_urls,
    entities_suggest_data,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.put(base_url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_change_without_changes(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        pk = api_client.get(
            base_url + "?description=" + entity_suggest_data["description"]
        ).data[0]["id"]
        url = base_url + f"/{pk}"
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["recaptcha"] = "test"
        response = api_client.put(url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["errorMessage"]
        assert str(response.data["errorMessage"][0]) == (
            "Todos os parâmetros da sugestão são iguais ao original! "
            "Por favor, altere algum campo para que a sugestão torne-se válida."
        )
        assert response.data["errorMessage"][0].code == "invalid"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_change(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        pk = api_client.get(
            base_url + "?description=" + entity_suggest_data["description"]
        ).data[0]["id"]
        url = base_url + f"/{pk}"
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["recaptcha"] = "test"
        entity_suggest_data["tags"] = ["Falta de decoro"]
        response = api_client.put(url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_200_OK
        assert list(response.data.keys()) == ["message"]
        assert (
            response.data["message"]
            == "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
        )


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_change_non_existing(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        model_name = base_url.split(f"/{API_BASE_URL}")[1].strip("/")[:-1]
        url = base_url + "/0"
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["recaptcha"] = "test"
        entity_suggest_data["tags"] = ["Fake news"]
        response = api_client.put(url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == [f"original_{model_name}"]
        assert (
            str(response.data[f"original_{model_name}"][0])
            == 'Pk inválido "0" - objeto não existe.'
        )
        assert response.data[f"original_{model_name}"][0].code == "does_not_exist"


def test_suggest_change_with_wrong_captcha(
    api_client,
    base_urls,
    entities_suggest_data,
):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        pk = api_client.get(
            base_url + "?description=" + entity_suggest_data["description"]
        ).data[0]["id"]
        url = base_url + f"/{pk}"
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["recaptcha"] = "test"
        entity_suggest_data["tags"] = ["Fake news"]
        response = api_client.put(url, data=entity_suggest_data)

        # THEN
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert (
            str(response.data["recaptcha"][0])
            == "Error verifying reCAPTCHA, please try again."
        )
        assert response.data["recaptcha"][0].code == "captcha_invalid"


def test_suggest_change_without_captcha(api_client, base_urls, entities_suggest_data):
    # GIVEN
    for base_url, entity_suggest_data in zip(base_urls, entities_suggest_data):

        # WHEN
        pk = api_client.get(
            base_url + "?description=" + entity_suggest_data["description"]
        ).data[0]["id"]
        url = base_url + f"/{pk}"
        entity_suggest_data["justification"] = "test"
        entity_suggest_data["tags"] = ["Fake news"]
        response = api_client.put(url, data=entity_suggest_data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert list(response.data.keys()) == ["recaptcha"]
        assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
        assert response.data["recaptcha"][0].code == "required"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_quote_without_fake_news_infos(
    api_client,
    quote_base_url,
    quote_suggest_data,
):
    # GIVEN

    # WHEN
    quote_suggest_data["recaptcha"] = "test"
    del quote_suggest_data["is_fake_news"]
    del quote_suggest_data["fake_news_source"]
    response = api_client.post(quote_base_url, data=quote_suggest_data)

    # THEN
    assert response.status_code == HTTP_200_OK
    assert list(response.data.keys()) == ["message"]
    assert (
        response.data["message"]
        == "Obrigado por contribuir! Aguarde mais informações por e-mail :)"
    )


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_quote_without_is_fake_news_with_fake_news_source(
    api_client,
    quote_base_url,
    quote_suggest_data,
):
    # GIVEN

    # WHEN
    quote_suggest_data["recaptcha"] = "test"
    del quote_suggest_data["is_fake_news"]
    response = api_client.post(quote_base_url, data=quote_suggest_data)

    # THEN
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert list(response.data.keys()) == ["is_fake_news"]
    assert str(response.data["is_fake_news"][0]) == (
        "Se há uma fonte compravando que é uma fake news, "
        "passe o parâmetro is_fake_news como True."
    )
    assert response.data["is_fake_news"][0].code == "invalid"


@override_settings(DRF_RECAPTCHA_TESTING=True)
def test_suggest_quote_without_without_fake_news_source_with_is_fake_news(
    api_client,
    quote_base_url,
    quote_suggest_data,
):
    # GIVEN

    # WHEN
    quote_suggest_data["recaptcha"] = "test"
    del quote_suggest_data["fake_news_source"]
    response = api_client.post(quote_base_url, data=quote_suggest_data)

    # THEN
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert list(response.data.keys()) == ["fake_news_source"]
    assert str(response.data["fake_news_source"][0]) == (
        "Se é uma fake news, forneça uma fonte que comprove a falsidade da declaração."
    )
    assert response.data["fake_news_source"][0].code == "invalid"


def test_suggest_quote_without_fake_news_infos_without_recaptcha(
    api_client, quote_base_url, quote_suggest_data
):
    # GIVEN

    # WHEN
    del quote_suggest_data["is_fake_news"]
    del quote_suggest_data["fake_news_source"]
    response = api_client.post(quote_base_url, data=quote_suggest_data)

    # THEN
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert list(response.data.keys()) == ["recaptcha"]
    assert str(response.data["recaptcha"][0]) == "Este campo é obrigatório."
    assert response.data["recaptcha"][0].code == "required"
