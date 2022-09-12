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


class YoutubeClipsResponse(Base):
    url: Optional[str]
    thumbnail_url: Optional[str]
    title: Optional[str]
    clip_id: Optional[str]
    video_id: Optional[str]
    kraken_posted: Optional[List[KrakenPosted]]


class YoutubeClipsResponsePagination(Base):
    youtube_response: List[YoutubeClipsResponse]
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
    TIKTOK = "TIKTOK"


class KrakenHead(Enum):
    TWITCH = "TWITCH"
    YOUTUBE = "YOUTUBE"


class PostInstagramClip(Base):
    id: Optional[int]
    url: str
    caption: str
    clip_id: str
    clip_name: str
    schedule: Optional[datetime.datetime]
    kraken_head: KrakenHead


class PostInstagramYoutubeClip(Base):
    youtube_clip_id: int
    caption: str


class PostTwitterClip(Base):
    id: Optional[int]
    twitter_handle: str
    url: str
    caption: str
    clip_id: str
    clip_name: str
    schedule: Optional[datetime.datetime]
    kraken_head: KrakenHead


class PostTiktokClip(Base):
    id: Optional[int]
    url: str
    caption: str
    clip_id: str
    clip_name: str
    schedule: Optional[datetime.datetime]
    kraken_head: KrakenHead


class AutomaticPostInstagramClip(Base):
    caption: Optional[str]
    creator_name: Optional[str]
    hours: int


class PostQueue(Base):
    id: int
    created_at: datetime.datetime
    post_status: PostStatus
    kraken_hand: KrakenHand
    name: Optional[str]
    schedule: Optional[datetime.datetime]


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


class CreateFollowInstagramTask(Base):
    username: str
    password: str
    use_same_db: Optional[bool]
    use_same_db_instagram_handle: Optional[str]
    instagram_handle: str
    tag: str
    activated: bool


class CreateTwitterFollowTask(Base):
    twitter_handle: str
    result_type: str
    tag: str


class GetTwitterSendMessageTask(Base):
    id: str
    total_sended: Optional[int]
    twitter_handle: str
    oauth_token: str
    oauth_secret: str
    consumer_key: str
    consumer_secret: str
    tag: str
    result_type: str
    message: str
    activated: bool


class GetTwitterFollowTask(Base):
    id: str
    twitter_handle: str
    oauth_token: str
    oauth_secret: str
    consumer_key: str
    consumer_secret: str
    tag: str
    result_type: str
    activated: bool


class GetInstagramFollowTask(Base):
    id: str
    instagram_handle: str
    tag: str
    activated: bool


class ParametersResponse(Base):
    id: int
    name: str
    activated: bool
    value: Optional[str]
    bool_value: Optional[float]
    int_value: Optional[int]


class CreateParameters(Base):
    name: str
    activated: bool
    value: Optional[str]
    bool_value: Optional[float]
    int_value: Optional[int]


class CutVideoYoutube(Base):
    youtube_id: str
    caption: str
    video_url: str
    start: int
    end: int


class DownloadVideoYoutube(Base):
    video_url: str
