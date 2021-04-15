import pytest

pytestmark = pytest.mark.django_db


def test_accept_suggestion(entities_suggestions):
    # GIVEN
    for entity_suggestion in entities_suggestions:
        # WHEN
        obj = entity_suggestion.accept()

        for field in obj._meta.get_fields():
            if field.name == "tags":
                obj_value = sorted(list(obj.tags_names))
                suggestion_value = sorted(list(entity_suggestion.tags_names))
            elif field.name in ("tagged_items", "id"):
                continue
            else:
                try:
                    obj_value = getattr(obj, field.name)
                    suggestion_value = getattr(entity_suggestion, field.name)
                except AttributeError:
                    continue

            # THEN
            assert obj_value == suggestion_value


def test_create_suggestion_without_additional_infos(entities_suggestions):
    # GIVEN
    for entity_suggestion in entities_suggestions:
        # WHEN
        entity_suggestion.additional_infos = ""
        entity_suggestion.save()
        obj = entity_suggestion.accept()

        # THEN
        assert not obj.additional_infos
        for field in obj._meta.get_fields():
            if field.name == "tags":
                obj_value = sorted(list(obj.tags_names))
                suggestion_value = sorted(list(entity_suggestion.tags_names))
            elif field.name in ("tagged_items", "id"):
                continue
            else:
                try:
                    obj_value = getattr(obj, field.name)
                    suggestion_value = getattr(entity_suggestion, field.name)
                except AttributeError:
                    continue

            assert obj_value == suggestion_value
