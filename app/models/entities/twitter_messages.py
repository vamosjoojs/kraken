from sqlalchemy import Column, String, Integer

from app.models.entities.base import BaseModel


class TwitterMessages(BaseModel):
    twitter_handle = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    message = Column(String, nullable=False)
    result_type = Column(String, nullable=False, server_default='mixed')
