from sqlalchemy import Column, String
from app.models.entities.base import BaseModel
from sqlalchemy.orm import relationship


class KrakenClips(BaseModel):
    clip_name = Column(String, nullable=False)
    clip_id = Column(String, nullable=False)
    clip_url = Column(String, nullable=False)
    thumbnail = Column(String)
    kraken_head = Column(String, nullable=False, server_default='TWITCH')
    kraken = relationship("Kraken", lazy="noload")
