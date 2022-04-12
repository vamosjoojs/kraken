from typing import List

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.db.repositories.twitter_send_message_repository import TwitterSendMessageRepository
from app.models.entities.twitter_tasks import TwitterTasks
from app.models.schemas.kraken import CreateTwitterSendMessageTask, GetTwitterSendMessageTask
from app import tasks


class TwitterServices:
    def __init__(self, auto_tasks_repo: AutoTasksRepository, twitter_tasks_repo: TwitterTasksRepository, twitter_send_message_repo: TwitterSendMessageRepository):
        self.auto_tasks_repo = auto_tasks_repo
        self.twitter_tasks_repo = twitter_tasks_repo
        self.twitter_send_message_repo = twitter_send_message_repo

    def create_send_message(self, create_twitter_send_message_task: CreateTwitterSendMessageTask) -> int:
        orm_model = TwitterTasks(**create_twitter_send_message_task.dict())
        self.twitter_tasks_repo.add(orm_model)
        return orm_model.id

    @staticmethod
    def trigger_send_message_task():
        tasks.twitter_send_message.apply_async(connect_timeout=10)

    def edit_send_message(self, id: int, edit_twitter_send_message_task: CreateTwitterSendMessageTask):
        orm_model = TwitterTasks(**edit_twitter_send_message_task.dict())
        id = self.twitter_tasks_repo.update_task(id, orm_model)
        return id

    def get_send_message(self) -> List[GetTwitterSendMessageTask]:
        orm_tasks = self.twitter_tasks_repo.get_tasks()
        response_list = []
        for data in orm_tasks:
            twitter_handle = data.twitter_handle
            if data.use_same_db:
                twitter_handle = data.use_same_db_twitter_handle
            total_sended = len(self.twitter_send_message_repo.get_users_by_twitter_handle(twitter_handle))
            response = GetTwitterSendMessageTask.from_orm(data)
            response.total_sended = total_sended
            response_list.append(response)
        return response_list
