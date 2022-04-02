from celery import Celery
from celery.schedules import crontab
from kombu import Queue
from app.config.config import config

# celery_queues = {"default": ("kraken", 2)}

app = Celery("broker", include=['app.tasks'])

# app.conf.task_acks_late = True
# app.conf.task_queues = (
#     Queue(q, routing_key="broker.#") for q, w in celery_queues.values()
# )
app.conf.update(broker_url=config.REDIS_URL,
                result_backend=config.REDIS_URL)

# app.conf.beat_schedule = {
#     'send-messages': {
#         'task': 'app.tasks.tasks.twitter_send_message',
#         'schedule': crontab(hour='*/2')
#     },
# }

# app.conf.task_default_queue = celery_queues["default"][0]
