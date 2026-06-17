from celery import Celery
from Core.settings import get_celery_broker_url, get_celery_backend_url

celery_app = Celery('Core', 
broker=get_celery_broker_url(), 
backend=get_celery_backend_url(),
include=['Tasks.test'])

celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Tasks.test.test',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

celery_app.conf.timezone = 'UTC'