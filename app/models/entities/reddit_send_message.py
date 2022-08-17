from sqlalchemy import Column, String, Boolean
from app.models.entities.base import BaseModel


class RedditSendMessage(BaseModel):
    user_id = Column(String, nullable=False)
    sended = Column(Boolean, nullable=False)
    reddit_handle = Column(String, nullable=False)
