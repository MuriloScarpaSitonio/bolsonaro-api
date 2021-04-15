from datetime import datetime, timedelta

import pytest

from .conftest import (
    ActionFactory,
    ActionSuggestionChangesFactory,
    QuoteFactory,
    QuoteSuggestionChangesFactory,
)

pytestmark = pytest.mark.django_db


def test_add_new_tag(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        tags = list(original_obj.tags_names) + ["Anvisa"]
        changes_obj.tags.add("Anvisa")
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["tags"]
        # testing this private method so we don't need to check if all other fields remain the same
        # in the original_obj
        changes_obj.accept()
        assert sorted(list(original_obj.tags_names)) == sorted(tags)


def test_remove_tag(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        tags = list(original_obj.tags_names)[:-1]
        changes_obj.tags.set(*tags)
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["tags"]
        changes_obj.accept()
        assert sorted(list(original_obj.tags_names)) == sorted(tags)


def test_change_date(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_date = original_obj.date + timedelta(days=1)
        changes_obj.date = new_date
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["date"]
        changes_obj.accept()
        assert original_obj.date == new_date


def test_date_is_estimated(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_date_is_estimated = not original_obj.date_is_estimated
        changes_obj.date_is_estimated = new_date_is_estimated
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["date_is_estimated"]
        changes_obj.accept()
        assert original_obj.date_is_estimated, new_date_is_estimated


def test_change_description(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_description = original_obj.description + "!!!!!"
        changes_obj.description = new_description
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["description"]
        changes_obj.accept()
        assert original_obj.description, new_description


def test_change_source(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_source = original_obj.source + "!!!!!"
        changes_obj.source = new_source
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["source"]
        changes_obj.accept()
        assert original_obj.source, new_source


def test_changes_additional_infos(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_additional_infos = original_obj.additional_infos + "!!!!!"
        changes_obj.additional_infos = new_additional_infos
        changes_obj.save()

        # THEN
        assert changes_obj._get_changes_fields_names() == ["additional_infos"]
        changes_obj.accept()
        assert original_obj.additional_infos, new_additional_infos


def test_change_multiple_fields(entities, entities_suggestions_change):

    # GIVEN
    for original_obj, changes_obj in zip(entities, entities_suggestions_change):

        # WHEN
        new_additional_infos = original_obj.additional_infos + "!!!!!"
        new_date_is_estimated = not original_obj.date_is_estimated
        new_date = original_obj.date + timedelta(days=1)
        new_tags = list(original_obj.tags_names) + ["STF"]

        changes_obj.additional_infos = new_additional_infos
        changes_obj.date_is_estimated = new_date_is_estimated
        changes_obj.date = new_date
        changes_obj.tags.add("STF")

        # THEN
        assert sorted(changes_obj._get_changes_fields_names()) == sorted(
            ["additional_infos", "date_is_estimated", "date", "tags"]
        )

        changes_obj.accept()
        assert original_obj.additional_infos == new_additional_infos
        assert original_obj.date_is_estimated == new_date_is_estimated
        assert original_obj.date == new_date
        assert sorted(list(original_obj.tags_names)) == sorted(new_tags)


def test_change_action_original_blank_fields(action_data, action_tags, user_email):

    # GIVEN
    additional_infos = action_data.pop("additional_infos")

    # WHEN

    date = datetime.strptime(action_data.pop("date"), "%d/%m/%Y")
    action_obj = ActionFactory(**{**action_data, "date": date})
    action_obj.tags.add(*action_tags)
    action_obj.save()

    changes_obj = ActionSuggestionChangesFactory(
        **{
            **action_data,
            "date": date,
            "additional_infos": additional_infos,
            "user_email": user_email,
            "original_action": action_obj,
            "justification": "test",
        }
    )
    changes_obj.tags.add(*action_tags)
    changes_obj.save()

    # THEN
    assert changes_obj._get_changes_fields_names() == ["additional_infos"]
    changes_obj.accept()
    assert action_obj.additional_infos == additional_infos


def test_change_quote_original_blank_fields(quote_data, quote_tags, user_email):
    # GIVEN
    is_fake_news = quote_data.pop("is_fake_news")
    fake_news_source = quote_data.pop("fake_news_source")

    # WHEN
    date = datetime.strptime(quote_data.pop("date"), "%d/%m/%Y")
    quote_obj = QuoteFactory(**{**quote_data, "date": date})
    quote_obj.tags.add(*quote_tags)
    quote_obj.save()

    changes_obj = QuoteSuggestionChangesFactory(
        **{
            **quote_data,
            "date": date,
            "is_fake_news": is_fake_news,
            "fake_news_source": fake_news_source,
            "user_email": user_email,
            "original_quote": quote_obj,
            "justification": "test",
        }
    )
    changes_obj.tags.add(*quote_tags)
    changes_obj.save()

    # THEN
    assert sorted(changes_obj._get_changes_fields_names()) == sorted(
        ["is_fake_news", "fake_news_source"]
    )
    changes_obj.accept()
    assert quote_obj.is_fake_news == is_fake_news
    assert quote_obj.fake_news_source == fake_news_source


def test_action_suggestion_changes_properties(action, action_suggestion_change):
    # GIVEN

    # WHEN

    # THEN
    assert action_suggestion_change.original_action_description == action.description
    assert action_suggestion_change.original_action_source == action.source
    assert action_suggestion_change.original_action_date == action.date
    assert (
        action_suggestion_change.original_action_date_is_estimated
        == action.date_is_estimated
    )
    assert (
        action_suggestion_change.original_action_additional_infos
        == action.additional_infos
    )
    assert action_suggestion_change.original_action_tags == ", ".join(action.tags_names)


def test_quote_suggestion_changes_properties(quote, quote_suggestion_change):
    # GIVEN

    # WHEN

    # THEN
    assert quote_suggestion_change.original_quote_description == quote.description
    assert quote_suggestion_change.original_quote_source == quote.source
    assert quote_suggestion_change.original_quote_date == quote.date
    assert (
        quote_suggestion_change.original_quote_date_is_estimated
        == quote.date_is_estimated
    )
    assert (
        quote_suggestion_change.original_quote_additional_infos
        == quote.additional_infos
    )
    assert quote_suggestion_change.original_quote_tags == ", ".join(quote.tags_names)
    assert (
        quote_suggestion_change.original_quote_fake_news_source
        == quote.fake_news_source
    )
    assert quote_suggestion_change.original_quote_is_fake_news == quote.is_fake_news
