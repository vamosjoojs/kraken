from sqlalchemy import Column, String, Integer

from app.models.entities.base import BaseModel


class TiktokTasks(BaseModel):
    tiktok_handle = Column(String, nullable=False)
    client_key = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    expires_in = Column(Integer, nullable=False)
    refresh_token = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    open_id = Column(String, nullable=False)
