from datetime import datetime, timedelta

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitch_repository import TwitchRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.integrations.twitter_integration import TwitterIntegration
from app.models.entities import Kraken, TwitchClips, AutoTasks
from app.models.schemas.kraken import (
    TwitchClipsResponse, PostInstagramClip, PostStatus, KrakenHand, TwitchClipsResponsePagination,
    AutomaticPostInstagramClip, PostTwitterClip, KrakenPosted,
)
from app.integrations.twitch_integration import TwitchIntegration
from app import tasks
from app.services.instagram_service import InstagramServices


class TwitchServices:
    def __init__(self, twitch_repo: TwitchRepository, kraken_repo: KrakenRepository, twitter_tasks_repo: TwitterTasksRepository,  auto_tasks_repo: AutoTasksRepository):
        self.twitch_integration = TwitchIntegration()
        self.twitch_repo = twitch_repo
        self.kraken_repo = kraken_repo
        self.twitter_tasks_repo = twitter_tasks_repo
        self.auto_tasks_repo = auto_tasks_repo

    def get_clips(self, next_cursor: str = None, back_cursor: str = None) -> TwitchClipsResponsePagination:
        clips = self.twitch_integration.get_all_clips(after_cursor=next_cursor, back_cursor=back_cursor)
        list_twitch_clip_response = []
        for clip in clips['data']:
            response_model = TwitchClipsResponse(**clip)
            response_model.clip_id = clip['id']
            clip_stored = self.twitch_repo.get_twitch_clips_by_clip_id(clip['id'])
            kraken_response = []
            if len(clip_stored) > 0:
                for clip in clip_stored:
                    if len(clip.kraken) > 0: # kraken e twitch clips é one-to-one
                        if clip.kraken[0].post_status != 'ERROR':
                            kraken_posted = KrakenPosted(
                                is_posted=True,
                                kraken_hand=clip.kraken[0].kraken_hand
                            )
                            kraken_response.append(kraken_posted)
            response_model.kraken_posted = kraken_response
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

    @staticmethod
    def post_clip_instagram_manual():
        instagram_services = InstagramServices()
        is_posted = instagram_services.post_clip('teste', r'C:\Users\davib\Documents\pessoal\bots\kraken\app\downloads\AT-cm_faBOl8RQXmF_cXyp4bJ3bA.mp4')
        if is_posted:
            print("fff")

    def post_clip_twitter(self, payload: PostTwitterClip):
        twitch_model = TwitchClips(
            clip_name=payload.clip_name,
            clip_id=payload.clip_id,
            clip_url=payload.thumbnail
        )

        twitch = self.twitch_repo.add(twitch_model)

        kraken_model = Kraken(
            post_status=PostStatus.CREATED.value,
            kraken_hand=KrakenHand.TWITTER.value,
            twitch_clips_id=twitch.id,
            caption=payload.caption
        )

        self.kraken_repo.add(kraken_model)

        clip_path = self.download_clip(payload.thumbnail)
        twitter_info = self.twitter_tasks_repo.get_task_by_twitter_handle(payload.twitter_handle)

        twitter_integration = TwitterIntegration(
            consumer_key=twitter_info.consumer_key,
            consumer_secret=twitter_info.consumer_secret,
            oauth_secret=twitter_info.oauth_secret,
            oauth_token=twitter_info.oauth_token
        )

        posted = twitter_integration.post_media(clip_path, payload.caption)

        if posted:
            kraken_model.post_status = PostStatus.COMPLETED.value
        else:
            kraken_model.post_status = PostStatus.ERROR.value
        self.kraken_repo.update_status(kraken_model)



