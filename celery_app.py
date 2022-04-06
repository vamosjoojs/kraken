from celery import Celery
from celery.schedules import crontab
from app.config.config import config

app = Celery("broker", include=['app.tasks'])


app.conf.update(broker_url=config.REDIS_URL,
                result_backend=config.REDIS_URL)

app.conf.beat_schedule = {
    'send-messages': {
        'task': 'app.tasks.tasks.twitter_send_message',
        'schedule': crontab(minute=0, hour='*/2')
    },
}
