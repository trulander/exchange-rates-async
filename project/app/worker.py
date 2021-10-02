import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from app.config import settings
from requests import Response, get

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
    result: Response = get(url=settings.url_to_endpoint_for_worker)
    print(result.status_code)
    if result.status_code == 200:
        return True
    return False