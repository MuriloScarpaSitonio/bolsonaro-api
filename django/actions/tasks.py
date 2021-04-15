from celery import shared_task

from helpers.tasks_helper import post_entity_tweet

from .views import ActionViewSet


@shared_task
def post_action_tweet() -> None:
    post_entity_tweet(view_set_obj=ActionViewSet())
