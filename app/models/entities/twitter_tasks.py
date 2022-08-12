from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.entities.base import BaseModel


class TwitterTasks(BaseModel):
    oauth_token = Column(String, nullable=False)
    oauth_secret = Column(String, nullable=False)
    consumer_key = Column(String, nullable=False)
    consumer_secret = Column(String, nullable=False)
    use_same_db = Column(Boolean, default=False)
    use_same_db_twitter_handle = Column(String)
    is_trending_user = Column(Boolean, default=False)
    twitter_handle = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)

    twitter_messages_id = Column(Integer, ForeignKey("twitter_messages.id"))
    twitter_messages = relationship("TwitterMessages", lazy="joined")

    twitter_follow_id = Column(Integer, ForeignKey("twitter_follow.id"))
    twitter_follow = relationship("TwitterFollow", lazy="joined")
