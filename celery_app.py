from celery import Celery
from celery.schedules import crontab
from app.config.config import config

app = Celery("broker", include=['app.tasks'])


app.conf.update(broker_url=config.REDIS_URL,
                result_backend=config.REDIS_URL)
