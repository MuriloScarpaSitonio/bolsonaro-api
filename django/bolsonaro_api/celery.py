import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bolsonaro_api.settings.production")

app = Celery("bolsonaro_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "post-action-tweet-every-day-at-8h": {
        "task": "actions.tasks.post_action_tweet",
        "schedule": crontab(minute=0, hour=11),  # UTC
    },
    "post-quote-tweet-every-day-at-18h": {
        "task": "quotes.tasks.post_quote_tweet",
        "schedule": crontab(minute=0, hour=21),  # UTC
    },
}
