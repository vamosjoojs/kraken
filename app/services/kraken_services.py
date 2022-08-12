from datetime import datetime, timedelta

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.integrations.twitch_integration import TwitchIntegration
from app.models.entities import KrakenClips, Kraken
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import PostQueue, PostStatus, KrakenHand, PostInstagramClip, KrakenHead, PostTwitterClip
from app import tasks


class KrakenServices:
    def __init__(self, kraken_repo: KrakenRepository, kraken_clips_repo: KrakenClipsRepository, twitter_tasks_repo: TwitterTasksRepository, auto_tasks_repo: AutoTasksRepository):
        self.kraken_repo = kraken_repo
        self.twitch_integration = TwitchIntegration()
        self.kraken_clips_repo = kraken_clips_repo
        self.kraken_repo = kraken_repo
        self.twitter_tasks_repo = twitter_tasks_repo
        self.auto_tasks_repo = auto_tasks_repo

    def get_posts_queue_async(self, page: int, page_size: int) -> Paginated[PostQueue]:
        queue_clips = self.kraken_repo.get_queue_posts(page, page_size)

        result_list = []
        for queue_clip in queue_clips.items:
            post_queue = PostQueue(
                created_at=queue_clip.created_at,
                post_status=PostStatus[queue_clip.post_status],
                kraken_hand=KrakenHand[queue_clip.kraken_hand],
                name=queue_clip.kraken_clips.clip_name,
                schedule=queue_clip.schedule
            )
            result_list.append(post_queue)

        return Paginated(
            total_items=queue_clips.total_items,
            total_pages=queue_clips.total_pages,
            current_page=queue_clips.current_page,
            items=result_list
        )

    def post_clip_instagram(self, payload: PostInstagramClip):
        if payload.schedule:
            payload.schedule = payload.schedule + timedelta(hours=3)
        kraken_model = self.create_kraken_and_clips(payload.clip_name,
                                                    payload.clip_id,
                                                    payload.url,
                                                    payload.caption,
                                                    KrakenHand.INSTAGRAM.value,
                                                    payload.kraken_head.value,
                                                    payload.id,
                                                    payload.schedule)
        payload = dict(payload)
        payload['kraken_id'] = kraken_model.id
        payload['kraken_head'] = kraken_model.kraken_head

        if payload['schedule']:
            tasks.post_instagram.apply_async(
                args=[dict(payload)], connect_timeout=10, eta=payload['schedule']
            )
        else:
            tasks.post_instagram.apply_async(
                args=[dict(payload)], connect_timeout=10
            )

    def post_clip_twitter(self, payload: PostTwitterClip):
        if payload.schedule:
            payload.schedule = payload.schedule + timedelta(hours=3)
        kraken_model = self.create_kraken_and_clips(payload.clip_name,
                                                    payload.clip_id,
                                                    payload.url,
                                                    payload.caption,
                                                    KrakenHand.TWITTER.value,
                                                    payload.kraken_head.value,
                                                    payload.id,
                                                    payload.schedule)

        payload = dict(payload)
        payload['kraken_id'] = kraken_model.id
        payload['kraken_head'] = kraken_model.kraken_head

        if payload['schedule']:
            tasks.post_twitter.apply_async(
                args=[dict(payload)], connect_timeout=10, eta=payload['schedule']
            )
        else:
            tasks.post_twitter.apply_async(
                args=[dict(payload)], connect_timeout=10
            )

    def create_kraken_and_clips(self,
                                clip_name: str,
                                clip_id: str,
                                url: str,
                                caption: str,
                                kraken_hand: KrakenHand,
                                kraken_head: KrakenHead,
                                id: int = None,
                                schedule: datetime = None) -> Kraken:
        if id:
            kraken_clips = self.kraken_clips_repo.get_clips_by_id(id)
        else:
            kraken_clips_model = KrakenClips(
                clip_name=clip_name,
                clip_id=clip_id,
                clip_url=url
            )

            kraken_clips = self.kraken_clips_repo.add(kraken_clips_model)

        kraken_model = Kraken(
            post_status=PostStatus.CREATED.value,
            kraken_hand=kraken_hand,
            kraken_head=kraken_head,
            kraken_clips_id=kraken_clips.id,
            caption=caption,
            schedule=schedule
        )

        self.kraken_repo.add(kraken_model)

        return kraken_model
