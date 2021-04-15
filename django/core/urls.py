from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path(
        "contribute/",
        TemplateView.as_view(template_name="index.html"),
        name="contribute",
    ),
    path(
        "legal-infos/",
        TemplateView.as_view(template_name="index.html"),
        name="legal_infos",
    ),
    path(
        "actions/",
        TemplateView.as_view(template_name="index.html"),
        name="actions_main",
    ),
    path(
        "actions/query/",
        TemplateView.as_view(template_name="index.html"),
        name="actions_query",
    ),
    path(
        "actions/<int:pk>/",
        TemplateView.as_view(template_name="index.html"),
        name="action_view",
    ),
    path(
        "quotes/", TemplateView.as_view(template_name="index.html"), name="quotes_main"
    ),
    path(
        "quotes/query/",
        TemplateView.as_view(template_name="index.html"),
        name="quotes_query",
    ),
    path(
        "quotes/<int:pk>/",
        TemplateView.as_view(template_name="index.html"),
        name="quote_view",
    ),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
