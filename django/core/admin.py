from typing import Dict, Tuple, Union

from actions.models import ActionSuggestion, ActionSuggestionChanges
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse

from quotes.models import QuoteSuggestion, QuoteSuggestionChanges
from .helpers.sendgrid_helper import (
    send_suggestion_accepted_email,
    send_suggestion_declined_email,
)


class EntityListFilter(admin.SimpleListFilter):
    """
    Classe que cria um filtro por tags em /admin
    """

    title = "Tags"
    parameter_name = "tag"

    def lookups(self, request: WSGIRequest, model_admin) -> Tuple[Tuple[str, str], ...]:
        """model_admin: Union[actions.admin.ActionAdmin, quotes.admin.QuoteAdmin]
        *Circular import error
        """
        tags = [tag.name for tag in self.tag_model.tags_for(model_admin.model)]
        tags.sort()
        return tuple(((tag, tag) for tag in tags))

    def queryset(self, request: WSGIRequest, queryset: QuerySet) -> QuerySet:
        value = self.value()
        return queryset.filter(tags__name=value) if value is not None else queryset


def _get_redirect_url(obj_name: str, splitter: str) -> str:
    path = [obj_name.split(splitter)[0], obj_name, "changelist"]
    return reverse(f"admin:{'_'.join(path)}")


class AbstractSuggestionAdmin(admin.ModelAdmin):
    """
    Classe que altera e expande algumas funcionalidades em /admin dos modelos Suggestion.
    """

    readonly_fields = ("user_email",)
    change_form_template = "custom_change_form_template.html"

    def response_change(
        self,
        request: WSGIRequest,
        obj: Union[ActionSuggestion, QuoteSuggestion],
    ) -> HttpResponseRedirect:

        if "decline-suggestion" in request.POST:
            send_suggestion_declined_email(
                request=request,
                user_email=obj.user_email,
                feedback=request.POST.get("decline-reasons"),
            )
            obj.delete()
            return HttpResponseRedirect(
                _get_redirect_url(
                    obj_name=obj.__class__.__name__.lower(), splitter="uggestion"
                )
            )

        if "accept-suggestion" in request.POST:
            created_obj = obj.accept()
            send_suggestion_accepted_email(
                request=request, user_email=obj.user_email, obj=created_obj
            )
            obj.delete()
            return HttpResponseRedirect(
                _get_redirect_url(
                    obj_name=obj.__class__.__name__.lower(), splitter="uggestion"
                )
            )
        return super().response_change(request, obj)


class AbstractSuggestionChangesAdmin(admin.ModelAdmin):
    """
    Classe que altera e expande algumas funcionalidades em /admin dos modelos SuggestionChanges.
    """

    change_form_template = "custom_change_form_template.html"
    fieldsets = (
        (
            "Mudanças sugeridas",
            {
                "fields": (),
            },
        ),
        ("Informações do usuário", {"fields": ("justification", "user_email")}),
    )
    readonly_fields = ("user_email", "justification")

    def get_fieldsets(
        self,
        request: WSGIRequest,
        obj: Union[ActionSuggestionChanges, QuoteSuggestionChanges] = None,
    ) -> Tuple[Tuple[str, Dict[str, Tuple[str, ...]]]]:

        fieldsets = super().get_fieldsets(request, obj)
        obj_name = obj.__class__.__name__.lower().split("suggestionchanges")[0]
        fields = tuple()  # type: tuple
        if obj:
            for field_name in obj._get_changes_fields_names():
                fields += ((field_name, "_".join(("original", obj_name, field_name))),)
        fieldsets[0][1]["fields"] = fields
        return fieldsets

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Union[ActionSuggestionChanges, QuoteSuggestionChanges] = None,
    ) -> Tuple[str, ...]:

        readonly_fields = super().get_readonly_fields(request, obj)
        obj_name = obj.__class__.__name__.lower().split("suggestionchanges")[0]
        if obj:
            for field_name in obj._get_changes_fields_names():
                readonly_fields += ("_".join(("original", obj_name, field_name)),)
        return readonly_fields

    def response_change(
        self,
        request: WSGIRequest,
        obj: Union[ActionSuggestionChanges, QuoteSuggestionChanges],
    ) -> HttpResponseRedirect:

        if "decline-suggestion" in request.POST:
            send_suggestion_declined_email(
                request=request,
                user_email=obj.user_email,
                feedback=request.POST.get("decline-reasons"),
            )
            obj.delete()
            return HttpResponseRedirect(
                _get_redirect_url(
                    obj_name=obj.__class__.__name__.lower(), splitter="uggestionchanges"
                )
            )

        if "accept-suggestion" in request.POST:
            original_obj = obj.accept()
            send_suggestion_accepted_email(
                request=request, user_email=obj.user_email, obj=original_obj
            )
            obj.delete()
            return HttpResponseRedirect(
                _get_redirect_url(
                    obj_name=obj.__class__.__name__.lower(), splitter="uggestionchanges"
                )
            )
        return super().response_change(request, obj)
