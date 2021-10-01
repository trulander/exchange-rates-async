import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from .config import settings

celery_log = get_task_logger(__name__)

app = Celery(
    'qwerty',
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    # include=['tasks']
)

app.conf.beat_schedule = {
    'default_task_event': {
        'task': 'default',
        'schedule': settings.celery_default_task_time_interval,
        'args': (),
    },
}
app.conf.timezone = 'UTC'

@app.task(name='default')
def get_rate() -> bool:

    return True