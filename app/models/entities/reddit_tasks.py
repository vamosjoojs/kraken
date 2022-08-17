from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.entities.base import BaseModel


class RedditTasks(BaseModel):
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reddit_handle = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)

    reddit_messages_id = Column(Integer, ForeignKey("reddit_messages.id"))
    reddit_messages = relationship("RedditMessages", lazy="joined")
