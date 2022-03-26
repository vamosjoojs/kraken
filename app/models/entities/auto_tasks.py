from sqlalchemy import Column, DateTime, String
from app.models.entities.base import BaseModel


class AutoTasks(BaseModel):
    post_type = Column(String, nullable=False)
    activated_at = Column(DateTime)
    deactivated_at = Column(DateTime)
    twitch_creator_name = Column(String, nullable=False)
