from sqlalchemy import Column, String, Boolean
from app.models.entities.base import BaseModel


class Twitch(BaseModel):
    clip_url = Column(String)
    post_status = Column(String, nullable=False)
    kraken_hand = Column(String, nullable=False)
