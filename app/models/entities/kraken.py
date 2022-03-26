from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.entities.base import BaseModel
from sqlalchemy.orm import relationship


class Kraken(BaseModel):
    post_status = Column(String, nullable=False)
    kraken_hand = Column(String, nullable=False)

    twitch_clips_id = Column(Integer, ForeignKey("twitch_clips.id"), nullable=False)
    twitch_clips = relationship("TwitchClips", lazy="noload", back_populates="kraken")

    caption = Column(String)
