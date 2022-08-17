from sqlalchemy import Column, String, Integer

from app.models.entities.base import BaseModel


class RedditMessages(BaseModel):
    reddit_handle = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    message = Column(String, nullable=False)
