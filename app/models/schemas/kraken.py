import datetime
from enum import Enum
from typing import Optional, List

from app.models.schemas.base import Base


class TwitchClipsResponse(Base):
    url: Optional[str]
    thumbnail_url: Optional[str]
    creator_name: Optional[str]
    title: Optional[str]


class TwitchClipsResponsePagination(Base):
    twitch_response: List[TwitchClipsResponse]
    cursor: Optional[str]


class PostStatus(Enum):
    CREATED = "CREATED"
    INITIATED = "INITIATED"
    DOWNLOADING_CLIP = "DOWNLOADING_CLIP"
    POSTING = "POSTING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class KrakenHand(Enum):
    INSTAGRAM = "INSTAGRAM"


class PostInstagramClip(Base):
    thumbnail: str
    caption: str


class PostQueue(Base):
    created_at: datetime.datetime
    post_status: PostStatus
    kraken_hand: KrakenHand
