from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from core.consts import API_BASE_URL

schema_view = get_schema_view(  # pylint: disable=invalid-name
    openapi.Info(
        title="Bolsonaro API",
        default_version="v1",
        description=(
            "API pública de declarações e ações do governo Bolsonaro.\n"
            "Entidade -> ação (action) ou declaração (quote)."
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def redirect_to_api_docs(_):
    return HttpResponseRedirect(API_BASE_URL + "docs/")


urlpatterns = [
    path("", redirect_to_api_docs),
    path("admin/", admin.site.urls),
    path(
        API_BASE_URL + "docs/",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="api_documentation",
    ),
    path(API_BASE_URL, include("quotes.urls")),
    path(API_BASE_URL, include("actions.urls")),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    re_path(
        ".*/", TemplateView.as_view(template_name="admin/404.html"), name="not_found"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
