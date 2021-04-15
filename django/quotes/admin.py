from core.admin import (
    AbstractSuggestionAdmin,
    AbstractSuggestionChangesAdmin,
    EntityListFilter,
)
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString

from .forms import QuoteAdminForm
from .models import (
    Quote,
    QuoteSuggestion,
    QuoteSuggestionChanges,
    QuoteTags,
    TaggedQuote,
)


class QuoteListFilter(EntityListFilter):
    tag_model = TaggedQuote


class QuoteAdmin(admin.ModelAdmin):
    form = QuoteAdminForm
    list_filter = (QuoteListFilter,)


class QuoteSuggestionAdmin(AbstractSuggestionAdmin):
    form = QuoteAdminForm
    list_filter = (QuoteListFilter,)


def link_to_original_quote(obj: QuoteSuggestionChanges) -> SafeString:
    id_ = obj.original_quote.id
    url = reverse("admin:quotes_quote_change", args=[id_])
    return format_html(f'<a href="{url}">Declaração {id_}</a>')


link_to_original_quote.description = "Link para declaração original"  # type: ignore


class QuoteSuggestionChangesAdmin(AbstractSuggestionChangesAdmin):
    """
    Classe que altera e expande algumas funcionalidades em /admin do modelo QuoteSuggestionChanges.
    """

    form = QuoteAdminForm
    list_display = ("description", link_to_original_quote)
    list_select_related = ("original_quote",)
    list_filter = (QuoteListFilter,)


admin.site.register(QuoteTags)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(QuoteSuggestion, QuoteSuggestionAdmin)
admin.site.register(QuoteSuggestionChanges, QuoteSuggestionChangesAdmin)
