from sqlalchemy import Column, String, Boolean
from app.models.entities.base import BaseModel


class TwitterTasks(BaseModel):
    oauth_token = Column(String, nullable=False)
    oauth_secret = Column(String, nullable=False)
    consumer_key = Column(String, nullable=False)
    consumer_secret = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    message = Column(String, nullable=False)
    twitter_handle = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)
    use_same_db = Column(Boolean, default=False)
    use_same_db_twitter_handle = Column(String)
