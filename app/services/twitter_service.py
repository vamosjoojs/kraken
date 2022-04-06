from typing import List

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.models.entities.twitter_tasks import TwitterTasks
from app.models.schemas.kraken import CreateTwitterSendMessageTask, GetTwitterSendMessageTask
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
        tasks.twitter_send_message.apply_async(connect_timeout=10)

    async def edit_send_message(self, id: int, edit_twitter_send_message_task: CreateTwitterSendMessageTask):
        orm_model = TwitterTasks(**edit_twitter_send_message_task.dict())
        id = await self.twitter_tasks_repo.update_task(id, orm_model)
        return id

    async def get_send_message(self) -> List[GetTwitterSendMessageTask]:
        orm_tasks = await self.twitter_tasks_repo.get_tasks()
        response_list = []
        for data in orm_tasks:
            response_list.append(
                GetTwitterSendMessageTask.from_orm(data)
            )
        return response_list
