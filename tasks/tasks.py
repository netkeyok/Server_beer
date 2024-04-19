from celery import Celery
from celery.schedules import crontab

from dbcon.config import REDIS_HOST, REDIS_PASS
from dbcon.functions import update_articles_name

celery_app = Celery('tasks', broker=f'redis://:{REDIS_PASS}@{REDIS_HOST}:6379/3')
celery_app.conf.timezone = 'Asia/Yekaterinburg'

celery_app.conf.beat_schedule = {
    'add-every-5-minutes': {
        'task': 'tasks.tasks.start_update_articles_name',
        'schedule': crontab(minute='*/5', hour='8-23'),
    },
}


@celery_app.task
def start_update_articles_name():
    result = update_articles_name()
    return result
