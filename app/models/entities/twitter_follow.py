from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.entities.base import BaseModel


class TwitterFollow(BaseModel):
    twitter_handle = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    result_type = Column(String, nullable=False, server_default='mixed')

