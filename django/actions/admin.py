from core.admin import (
    AbstractSuggestionAdmin,
    AbstractSuggestionChangesAdmin,
    EntityListFilter,
)
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

from .forms import ActionAdminForm
from .models import (
    Action,
    ActionSuggestion,
    ActionSuggestionChanges,
    ActionTags,
    TaggedAction,
)


class ActionListFilter(EntityListFilter):
    tag_model = TaggedAction


class ActionAdmin(admin.ModelAdmin):
    form = ActionAdminForm
    list_filter = (ActionListFilter,)


class ActionSuggestionAdmin(AbstractSuggestionAdmin):
    form = ActionAdminForm
    list_filter = (ActionListFilter,)


def link_to_original_action(obj: ActionSuggestionChanges) -> SafeString:
    id_ = obj.original_action.id
    url = reverse("admin:actions_action_change", args=[id_])
    return format_html(f'<a href="{url}">Ação {id_}</a>')


link_to_original_action.description = "Link para ação original"  # type: ignore


class ActionSuggestionChangesAdmin(AbstractSuggestionChangesAdmin):
    """
    Classe que altera e expande algumas funcionalidades em /admin do modelo ActionSuggestionChanges.
    """

    form = ActionAdminForm
    list_display = ("description", link_to_original_action)
    list_select_related = ("original_action",)
    list_filter = (ActionListFilter,)


admin.site.register(ActionTags)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionSuggestion, ActionSuggestionAdmin)
admin.site.register(ActionSuggestionChanges, ActionSuggestionChangesAdmin)
