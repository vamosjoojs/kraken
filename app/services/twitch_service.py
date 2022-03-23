from app.db.repositories.twitch_repository import TwitchRepository
from app.models.entities import Twitch
from app.models.schemas.kraken import (
    TwitchClipsResponse, PostInstagramClip, PostStatus, KrakenHand, TwitchClipsResponsePagination,
)
from typing import List
from app.integrations.twitch_integration import TwitchIntegration
from app import tasks


class TwitchServices:
    def __init__(self, repo: TwitchRepository):
        self.twitch_integration = TwitchIntegration()
        self.repo = repo

    def get_clips(self, next_cursor: str = None, back_cursor: str = None) -> TwitchClipsResponsePagination:
        clips = self.twitch_integration.get_all_clips(after_cursor=next_cursor, back_cursor=back_cursor)
        list_twitch_clip_response = []
        for clip in clips['data']:
            response_model = TwitchClipsResponse(**clip)
            list_twitch_clip_response.append(response_model)

        response = TwitchClipsResponsePagination(twitch_response=list_twitch_clip_response, cursor=clips['pagination']['cursor'])
        return response

    def download_clip(self, thumbnail: str) -> str:
        clip_path = self.twitch_integration.download_clip(thumbnail)
        return clip_path

    async def post_clip_instagram(self, payload: PostInstagramClip):
        clip = await self.repo.get_twitch_clips_by_clip_url(payload.thumbnail)
        if clip and clip.kraken_hand == KrakenHand.INSTAGRAM.value and clip.clip_url == payload.thumbnail:
            raise "Video já postado no Instagram."

        twitch_model = Twitch(post_status=PostStatus.CREATED.value,
                              kraken_hand=KrakenHand.INSTAGRAM.value,
                              clip_url=payload.thumbnail)

        id = await self.repo.insert_or_update(twitch_model)

        payload = dict(payload)
        payload['id'] = id

        tasks.post_instagram.apply_async(
            args=[dict(payload)], connect_timeout=10
        )

