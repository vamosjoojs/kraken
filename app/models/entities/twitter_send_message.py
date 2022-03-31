from sqlalchemy import Column, String, Boolean, BigInteger
from app.models.entities.base import BaseModel


class TwitterSendMessage(BaseModel):
    user_id = Column(BigInteger, nullable=False)
    sended = Column(Boolean, nullable=False)
    twitter_handle = Column(String, nullable=False)
