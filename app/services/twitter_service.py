from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.models.entities.twitter_tasks import TwitterTasks
from app.models.schemas.kraken import CreateTwitterSendMessageTask
from app import tasks


class TwitterServices:
    def __init__(self, auto_tasks_repo: AutoTasksRepository, twitter_tasks_repo: TwitterTasksRepository):
        self.auto_tasks_repo = auto_tasks_repo
        self.twitter_tasks_repo = twitter_tasks_repo

    async def create_send_message(self, create_twitter_send_message_task: CreateTwitterSendMessageTask) -> int:
        orm_model = TwitterTasks(**create_twitter_send_message_task.dict())
        await self.twitter_tasks_repo.add(orm_model)
        return orm_model.id

    async def trigger_send_message_task(self):
        tasks_send_message = await self.twitter_tasks_repo.get_tasks()
        for task in tasks_send_message:
            payload = {
                'twitter_handler': task.twitter_handle,
                'tag': task.tag,
                'message': task.message,
                'consumer_key': task.consumer_key,
                'consumer_secret': task.consumer_secret,
                'oauth_token': task.oauth_token,
                'oauth_secret': task.oauth_secret
            }
            tasks.twitter_send_message.apply_async(
                args=[dict(payload)], connect_timeout=10
            )
