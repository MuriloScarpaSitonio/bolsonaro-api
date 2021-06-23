import pytest

from actions.admin import (
    ActionListFilter,
    ActionSuggestionAdmin,
    ActionSuggestionChangesAdmin,
)
from actions.models import Action, ActionSuggestion, ActionSuggestionChanges
from django.contrib.admin.sites import AdminSite
from quotes.admin import (
    QuoteListFilter,
    QuoteSuggestionAdmin,
    QuoteSuggestionChangesAdmin,
)
from quotes.models import Quote, QuoteSuggestion, QuoteSuggestionChanges

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "admin_model, model, url",
    [
        (ActionSuggestionAdmin, ActionSuggestion, "/admin/actions/actionsuggestion/"),
        (QuoteSuggestionAdmin, QuoteSuggestion, "/admin/quotes/quotesuggestion/"),
    ],
)
def test_decline_suggestion_admin(
    mocker,
    action_suggestion,
    quote_suggestion,
    admin_model,
    model,
    url,
    decline_suggestion_request,
):
    # GIVEN
    obj = action_suggestion if model == ActionSuggestion else quote_suggestion
    admin_view = admin_model(model=model, admin_site=AdminSite())
    mocker.patch("core.admin.send_suggestion_declined_email")
    response = mocker.patch("core.admin.HttpResponseRedirect")

    # WHEN
    admin_view.response_change(request=decline_suggestion_request, obj=obj)

    # THEN
    assert not model.objects.exists()
    assert response.call_args[0][0] == url


@pytest.mark.parametrize(
    "admin_model, model, original_model, url",
    [
        (
            ActionSuggestionAdmin,
            ActionSuggestion,
            Action,
            "/admin/actions/actionsuggestion/",
        ),
        (
            QuoteSuggestionAdmin,
            QuoteSuggestion,
            Quote,
            "/admin/quotes/quotesuggestion/",
        ),
    ],
)
def test_accept_suggestion_admin(
    mocker,
    action_suggestion,
    quote_suggestion,
    admin_model,
    model,
    original_model,
    url,
    accept_suggestion_request,
):
    # GIVEN
    number_of_objs = original_model.objects.count()
    obj = action_suggestion if model == ActionSuggestion else quote_suggestion
    admin_view = admin_model(model=model, admin_site=AdminSite())
    mocker.patch("core.admin.send_suggestion_accepted_email")
    response = mocker.patch("core.admin.HttpResponseRedirect")

    # WHEN
    admin_view.response_change(request=accept_suggestion_request, obj=obj)

    # THEN
    assert not model.objects.exists()
    assert response.call_args[0][0] == url
    assert original_model.objects.count() == number_of_objs + 1


@pytest.mark.parametrize(
    "admin_model, model, name",
    [
        (ActionSuggestionChangesAdmin, ActionSuggestionChanges, "action"),
        (QuoteSuggestionChangesAdmin, QuoteSuggestionChanges, "quote"),
    ],
)
def test_get_fieldsets_suggestion_change_admin(
    admin_model,
    model,
    name,
    action_suggestion_change,
    quote_suggestion_change,
    wsgi_request,
):
    # GIVEN
    obj = (
        action_suggestion_change
        if model == ActionSuggestionChanges
        else quote_suggestion_change
    )
    obj.description = "!!!"
    admin_view = admin_model(model=model, admin_site=AdminSite())

    # WHEN
    fieldsets = admin_view.get_fieldsets(request=wsgi_request, obj=obj)

    # THEN
    assert fieldsets == (
        (
            "Mudanças sugeridas",
            {"fields": (("description", f"original_{name}_description"),)},
        ),
        ("Informações do usuário", {"fields": ("justification", "user_email")}),
    )


@pytest.mark.parametrize(
    "admin_model, model, name",
    [
        (ActionSuggestionChangesAdmin, ActionSuggestionChanges, "action"),
        (QuoteSuggestionChangesAdmin, QuoteSuggestionChanges, "quote"),
    ],
)
def test_get_readonly_fields_suggestion_change_admin(
    admin_model,
    model,
    name,
    action_suggestion_change,
    quote_suggestion_change,
    wsgi_request,
):
    # GIVEN
    obj = (
        action_suggestion_change
        if model == ActionSuggestionChanges
        else quote_suggestion_change
    )
    obj.description = "!!!"
    admin_view = admin_model(model=model, admin_site=AdminSite())

    # WHEN
    readonly_fields = admin_view.get_readonly_fields(request=wsgi_request, obj=obj)

    # THEN
    assert readonly_fields == (
        "user_email",
        "justification",
        f"original_{name}_description",
    )


@pytest.mark.parametrize(
    "admin_model, model, url",
    [
        (
            ActionSuggestionChangesAdmin,
            ActionSuggestionChanges,
            "/admin/actions/actionsuggestionchanges/",
        ),
        (
            QuoteSuggestionChangesAdmin,
            QuoteSuggestionChanges,
            "/admin/quotes/quotesuggestionchanges/",
        ),
    ],
)
def test_decline_suggestion_change_admin(
    mocker,
    admin_model,
    model,
    url,
    action_suggestion_change,
    quote_suggestion_change,
    decline_suggestion_request,
):
    # GIVEN
    obj = (
        action_suggestion_change
        if model == ActionSuggestionChanges
        else quote_suggestion_change
    )
    admin_view = admin_model(model=model, admin_site=AdminSite())
    mocker.patch("core.admin.send_suggestion_declined_email")
    response = mocker.patch("core.admin.HttpResponseRedirect")

    # WHEN
    admin_view.response_change(request=decline_suggestion_request, obj=obj)

    # THEN
    assert not model.objects.exists()
    assert response.call_args[0][0] == url


@pytest.mark.parametrize(
    "admin_model, model, url",
    [
        (
            ActionSuggestionChangesAdmin,
            ActionSuggestionChanges,
            "/admin/actions/actionsuggestionchanges/",
        ),
        (
            QuoteSuggestionChangesAdmin,
            QuoteSuggestionChanges,
            "/admin/quotes/quotesuggestionchanges/",
        ),
    ],
)
def test_accept_suggestion_change_admin(
    mocker,
    admin_model,
    model,
    url,
    action,
    action_suggestion_change,
    quote,
    quote_suggestion_change,
    accept_suggestion_request,
):
    # GIVEN
    if model == ActionSuggestionChanges:
        obj = action_suggestion_change
        original_obj = action
    else:
        obj = quote_suggestion_change
        original_obj = quote

    obj.description = "!!!"
    obj.save()
    admin_view = admin_model(model=model, admin_site=AdminSite())
    mocker.patch("core.admin.send_suggestion_accepted_email")
    response = mocker.patch("core.admin.HttpResponseRedirect")

    # WHEN
    admin_view.response_change(
        request=accept_suggestion_request,
        obj=obj,
    )

    # THEN
    assert not model.objects.exists()
    assert original_obj.description == "!!!"
    assert response.call_args[0][0] == url


@pytest.mark.parametrize(
    "admin_model, model, filter_model",
    [
        (ActionSuggestionAdmin, ActionSuggestion, ActionListFilter),
        (QuoteSuggestionAdmin, QuoteSuggestion, QuoteListFilter),
    ],
)
def test_get_lookups_filter_admin(
    admin_model,
    model,
    filter_model,
    action_suggestion,
    quote_suggestion,
    wsgi_request,
):
    obj = action_suggestion if model == ActionSuggestion else quote_suggestion
    filter_instance = filter_model(
        request=wsgi_request,
        params={},
        model=model,
        model_admin=admin_model(model=model, admin_site=AdminSite()),
    )
    # GIVEN
    lookups = filter_instance.lookup_choices

    # THEN
    assert lookups == list(((tag, tag) for tag in sorted(obj.tags_names)))


@pytest.mark.parametrize(
    "admin_model, model, filter_model, mocker_path",
    [
        (
            ActionSuggestionAdmin,
            ActionSuggestion,
            ActionListFilter,
            "actions.admin.ActionListFilter.value",
        ),
        (
            QuoteSuggestionAdmin,
            QuoteSuggestion,
            QuoteListFilter,
            "quotes.admin.QuoteListFilter.value",
        ),
    ],
)
def test_filter_queryset(
    mocker,
    admin_model,
    model,
    filter_model,
    mocker_path,
    action_suggestion,  # pylint: disable=unused-argument
    quote_suggestion,  # pylint: disable=unused-argument
    wsgi_request,
):
    request = wsgi_request
    filter_instance = filter_model(
        request=request,
        params={},
        model=model,
        model_admin=admin_model(model=model, admin_site=AdminSite()),
    )
    mocker.patch(mocker_path, return_value="Test")

    queryset = filter_instance.queryset(request=request, queryset=model.objects.all())
    assert not queryset.exists()
