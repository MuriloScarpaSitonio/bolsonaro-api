from celery import shared_task

from helpers.tasks_helper import post_entity_tweet

from .views import QuoteViewSet


@shared_task
def post_quote_tweet() -> None:
    post_entity_tweet(view_set_obj=QuoteViewSet())
