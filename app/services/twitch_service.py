from datetime import datetime, timedelta

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitch_repository import TwitchRepository
from app.models.entities import Kraken, TwitchClips, AutoTasks
from app.models.schemas.kraken import (
    TwitchClipsResponse, PostInstagramClip, PostStatus, KrakenHand, TwitchClipsResponsePagination,
    AutomaticPostInstagramClip,
)
from app.integrations.twitch_integration import TwitchIntegration
from app import tasks


class TwitchServices:
    def __init__(self, twitch_repo: TwitchRepository, kraken_repo: KrakenRepository, auto_tasks_repo: AutoTasksRepository):
        self.twitch_integration = TwitchIntegration()
        self.twitch_repo = twitch_repo
        self.kraken_repo = kraken_repo
        self.auto_tasks_repo = auto_tasks_repo

    def get_clips(self, next_cursor: str = None, back_cursor: str = None) -> TwitchClipsResponsePagination:
        clips = self.twitch_integration.get_all_clips(after_cursor=next_cursor, back_cursor=back_cursor)
        list_twitch_clip_response = []
        for clip in clips['data']:
            response_model = TwitchClipsResponse(**clip)
            response_model.clip_id = clip['id']
            clip_stored = self.twitch_repo.get_twitch_clips_by_clip_id(clip['id'])
            response_model.is_posted = False
            if clip_stored and clip_stored.kraken[0].post_status != 'ERROR':
                response_model.is_posted = True
                response_model.kraken_hand = clip_stored.kraken[0].kraken_hand
            list_twitch_clip_response.append(response_model)

        response = TwitchClipsResponsePagination(twitch_response=list_twitch_clip_response, cursor=clips['pagination']['cursor'])
        return response

    def download_clip(self, thumbnail: str) -> str:
        clip_path = self.twitch_integration.download_clip(thumbnail)
        return clip_path

    def post_clip_instagram(self, payload: PostInstagramClip):
        twitch_model = TwitchClips(
            clip_name=payload.clip_name,
            clip_id=payload.clip_id,
            clip_url=payload.thumbnail
        )

        twitch = self.twitch_repo.add(twitch_model)

        kraken_model = Kraken(
            post_status=PostStatus.CREATED.value,
            kraken_hand=KrakenHand.INSTAGRAM.value,
            twitch_clips_id=twitch.id,
            caption=payload.caption
        )

        kraken = self.kraken_repo.add(kraken_model)

        payload = dict(payload)
        payload['kraken_id'] = kraken.id

        tasks.post_instagram.apply_async(
            args=[dict(payload)], connect_timeout=10
        )

    def automatic_post_clip_instagram(self, payload: AutomaticPostInstagramClip):
        switch_instagram = AutoTasks(
            post_type="INSTAGRAM",
            twitch_creator_name=payload.creator_name,
            activated_at=datetime.utcnow(),
            deactivated_at=datetime.utcnow() + timedelta(hours=payload.hours)
        )
        self.auto_tasks_repo.add(switch_instagram)

        payload = dict(payload)
        payload['auto_task_id'] = switch_instagram.id
        payload['initial_date'] = datetime.now()

        tasks.automatic_post_instagram.apply_async(
            args=[payload], connect_timeout=10
        )
        return switch_instagram.id

    def disable_automatic_post_clip_instagram(self, id: int):
        self.auto_tasks_repo.disable_task(id)

