from typing import List

from app.db.repositories.instagram_tasks_repository import InstagramTasksRepository
from app.models.entities import InstagramFollow, InstagramTasks
from app.models.schemas.kraken import CreateFollowInstagramTask, GetInstagramFollowTask
from app import tasks


class InstagramBotServices:
    def __init__(self, instagram_tasks_repo: InstagramTasksRepository):
        self.instagram_tasks_repo = instagram_tasks_repo

    def create_follow_task(self, create_follow_task: CreateFollowInstagramTask) -> int:
        instagram_follow_orm = InstagramFollow(
            instagram_handle=create_follow_task.instagram_handle,
            tag=create_follow_task.tag,
        )

        orm_model = InstagramTasks(**create_follow_task.dict(exclude={"tag"}))
        orm_model.instagram_follow = instagram_follow_orm

        self.instagram_tasks_repo.add(orm_model)
        return orm_model.id

    def edit_follow(self, id: int, edit_follow_task: CreateFollowInstagramTask):
        instagram_follow_orm = InstagramFollow(
            instagram_handle=edit_follow_task.instagram_handle,
            tag=edit_follow_task.tag,
        )

        orm_model = InstagramTasks(**edit_follow_task.dict(exclude={"tag"}))
        orm_model.instagram_follow = instagram_follow_orm
        id = self.instagram_tasks_repo.update_follow_task(id, orm_model)
        return id

    @staticmethod
    def trigger_follow_task():
        tasks.instagram_follow.apply_async(connect_timeout=10)

    def get_follow(self) -> List[GetInstagramFollowTask]:
        orm_tasks = self.instagram_tasks_repo.get_tasks()
        response_list = []
        for data in orm_tasks:
            if data.instagram_follow:
                response = GetInstagramFollowTask(
                    id=data.id,
                    instagram_handle=data.instagram_handle,
                    tag=data.instagram_follow.tag,
                    activated=data.activated
                )
                response_list.append(response)
        return response_list
