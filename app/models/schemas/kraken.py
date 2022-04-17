import datetime
from enum import Enum
from typing import Optional, List

from app.models.schemas.base import Base


class KrakenPosted(Base):
    is_posted: bool
    kraken_hand: str


class TwitchClipsResponse(Base):
    url: Optional[str]
    thumbnail_url: Optional[str]
    creator_name: Optional[str]
    title: Optional[str]
    clip_id: Optional[str]
    kraken_posted: Optional[List[KrakenPosted]]


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
    TWITTER = "TWITTER"


class PostInstagramClip(Base):
    thumbnail: str
    caption: str
    clip_id: str
    clip_name: str


class PostTwitterClip(Base):
    twitter_handle: str
    thumbnail: str
    caption: str
    clip_id: str
    clip_name: str


class AutomaticPostInstagramClip(Base):
    caption: Optional[str]
    creator_name: Optional[str]
    hours: int


class PostQueue(Base):
    created_at: datetime.datetime
    post_status: PostStatus
    kraken_hand: KrakenHand
    name: Optional[str]


class CreateTwitterSendMessageTask(Base):
    twitter_handle: str
    result_type: str
    oauth_token: str
    oauth_secret: str
    consumer_key: str
    consumer_secret: str
    tag: str
    message: str
    activated: bool


class GetTwitterSendMessageTask(Base):
    id: str
    total_sended: Optional[int]
    twitter_handle: str
    oauth_token: str
    oauth_secret: str
    consumer_key: str
    consumer_secret: str
    tag: str
    message: str
    activated: bool
