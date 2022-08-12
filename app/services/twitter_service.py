from typing import List

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.db.repositories.twitter_send_message_repository import (
    TwitterSendMessageRepository,
)
from app.models.entities import TwitterMessages, TwitterFollow
from app.models.entities.twitter_tasks import TwitterTasks
from app.models.schemas.kraken import (
    CreateTwitterSendMessageTask,
    GetTwitterSendMessageTask,
    CreateTwitterFollowTask,
    GetTwitterFollowTask,
)
from app import tasks


class TwitterServices:
    def __init__(
        self,
        auto_tasks_repo: AutoTasksRepository,
        twitter_tasks_repo: TwitterTasksRepository,
        twitter_send_message_repo: TwitterSendMessageRepository,
    ):
        self.auto_tasks_repo = auto_tasks_repo
        self.twitter_tasks_repo = twitter_tasks_repo
        self.twitter_send_message_repo = twitter_send_message_repo

    def create_send_message(
        self, create_twitter_send_message_task: CreateTwitterSendMessageTask
    ) -> int:
        twitter_message_orm = TwitterMessages(
            twitter_handle=create_twitter_send_message_task.twitter_handle,
            tag=create_twitter_send_message_task.tag,
            message=create_twitter_send_message_task.message,
            result_type=create_twitter_send_message_task.result_type,
        )

        orm_model = TwitterTasks(
            **create_twitter_send_message_task.dict(
                exclude={"result_type", "tag", "message"}
            )
        )
        orm_model.twitter_messages = twitter_message_orm

        self.twitter_tasks_repo.add(orm_model)
        return orm_model.id

    @staticmethod
    def trigger_send_message_task():
        tasks.twitter_send_message.apply_async(connect_timeout=10)

    def edit_send_message(
        self, id: int, edit_twitter_send_message_task: CreateTwitterSendMessageTask
    ):
        twitter_message_orm = TwitterMessages(
            twitter_handle=edit_twitter_send_message_task.twitter_handle,
            tag=edit_twitter_send_message_task.tag,
            message=edit_twitter_send_message_task.message,
            result_type=edit_twitter_send_message_task.result_type,
        )

        orm_model = TwitterTasks(
            **edit_twitter_send_message_task.dict(
                exclude={"result_type", "tag", "message"}
            )
        )
        orm_model.twitter_messages = twitter_message_orm
        id = self.twitter_tasks_repo.update_message_task(id, orm_model)
        return id

    def get_send_message(self) -> List[GetTwitterSendMessageTask]:
        orm_tasks = self.twitter_tasks_repo.get_tasks()
        response_list = []
        for data in orm_tasks:
            twitter_handle = data.twitter_handle
            if data.use_same_db:
                twitter_handle = data.use_same_db_twitter_handle
            total_sended = len(
                self.twitter_send_message_repo.get_users_by_twitter_handle(
                    twitter_handle
                )
            )
            response = GetTwitterSendMessageTask(
                id=data.id,
                total_sended=total_sended,
                twitter_handle=data.twitter_handle,
                oauth_token=data.oauth_token,
                oauth_secret=data.oauth_secret,
                consumer_key=data.consumer_key,
                consumer_secret=data.consumer_secret,
                tag=data.twitter_messages.tag,
                result_type=data.twitter_messages.result_type,
                message=data.twitter_messages.message,
                activated=data.activated,
            )
            response_list.append(response)
        return response_list

    def create_follow(self, create_twitter_follow_task: CreateTwitterFollowTask):
        twitter_follow_orm = TwitterFollow(
            twitter_handle=create_twitter_follow_task.twitter_handle,
            tag=create_twitter_follow_task.twitter_handle,
            result_type=create_twitter_follow_task.result_type,
        )

        return self.twitter_tasks_repo.add_follow(
            create_twitter_follow_task.twitter_handle, twitter_follow_orm
        )

    @staticmethod
    def trigger_follow_task():
        tasks.twitter_follow.apply_async(connect_timeout=10)

    def get_follow(self):
        orm_tasks = self.twitter_tasks_repo.get_tasks()
        response_list = []
        for data in orm_tasks:
            if data.twitter_follow:
                response = GetTwitterFollowTask(
                    id=data.id,
                    twitter_handle=data.twitter_handle,
                    oauth_token=data.oauth_token,
                    oauth_secret=data.oauth_secret,
                    consumer_key=data.consumer_key,
                    consumer_secret=data.consumer_secret,
                    tag=data.twitter_follow.tag,
                    result_type=data.twitter_follow.result_type,
                    activated=data.activated,
                )
                response_list.append(response)
        return response_list
