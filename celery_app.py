from celery import Celery
from celery.schedules import crontab
from app.config.config import config

app = Celery("broker", include=['app.tasks'])


app.conf.update(broker_url=config.REDIS_URL,
                result_backend=config.REDIS_URL)

app.conf.broker_transport_options = {'visibility_timeout': 2592000}
app.conf.result_backend_transport_options = {'result_chord_ordered': True}
app.conf.worker_prefetch_multiplier = 1

app.conf.beat_schedule = {
    'send-messages': {
        'task': 'app.tasks.tasks.twitter_send_message',
        'schedule': crontab(minute=0, hour='*/2')
    }
}