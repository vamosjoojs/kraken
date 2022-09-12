from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.models.entities.base import BaseModel
from sqlalchemy.orm import relationship


class Kraken(BaseModel):
    post_status = Column(String, nullable=False)
    kraken_hand = Column(String, nullable=False)

    kraken_clips_id = Column(Integer, ForeignKey("kraken_clips.id"))
    kraken_clips = relationship("KrakenClips", lazy="noload", back_populates="kraken")

    caption = Column(String)
    schedule = Column(DateTime)
