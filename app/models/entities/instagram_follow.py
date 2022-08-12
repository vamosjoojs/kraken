from sqlalchemy import Column, String

from app.models.entities.base import BaseModel


class InstagramFollow(BaseModel):
    instagram_handle = Column(String, nullable=False)
    tag = Column(String, nullable=False)
