from datetime import datetime, timedelta, date

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.tiktok_tasks_repository import TiktokTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.integrations.twitch_integration import TwitchIntegration
from app.models.entities import KrakenClips, Kraken
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import PostQueue, PostStatus, KrakenHand, PostInstagramClip, KrakenHead, PostTwitterClip, \
    PostChangeStatus, GetPostByMonth, PostsDetail
from app import tasks
import calendar
from collections import defaultdict


class KrakenServices:
    def __init__(self, kraken_repo: KrakenRepository, kraken_clips_repo: KrakenClipsRepository, twitter_tasks_repo: TwitterTasksRepository, auto_tasks_repo: AutoTasksRepository, tiktok_repo: TiktokTasksRepository):
        self.kraken_repo = kraken_repo
        self.twitch_integration = TwitchIntegration()
        self.kraken_clips_repo = kraken_clips_repo
        self.kraken_repo = kraken_repo
        self.twitter_tasks_repo = twitter_tasks_repo
        self.auto_tasks_repo = auto_tasks_repo
        self.tiktok_repo = tiktok_repo

    def get_posts_queue_async(self, page: int, page_size: int) -> Paginated[PostQueue]:
        queue_clips = self.kraken_repo.get_queue_posts(page, page_size)

        result_list = []
        for queue_clip in queue_clips.items:
            post_queue = PostQueue(
                id=queue_clip.kraken_clips_id,
                created_at=queue_clip.created_at,
                post_status=PostStatus[queue_clip.post_status],
                kraken_hand=KrakenHand[queue_clip.kraken_hand],
                name=queue_clip.caption,
                schedule=queue_clip.schedule
            )
            result_list.append(post_queue)

        return Paginated(
            total_items=queue_clips.total_items,
            total_pages=queue_clips.total_pages,
            current_page=queue_clips.current_page,
            items=result_list
        )

    def get_posts_by_date(self, date: date, post_status: PostStatus) -> GetPostByMonth:
        range_date = calendar.monthrange(date.year, date.month)
        queue_clips = self.kraken_repo.get_queue_post_by_date(initial_date=date.replace(day=range_date[0]+1), finish_date=date.replace(day=range_date[1]), post_status=post_status.value)

        contagem_kraken_hand = defaultdict(int)

        for objeto in queue_clips:
            kraken_hand = objeto.kraken_hand
            contagem_kraken_hand[kraken_hand] += 1

        post_detail = []
        for kraken_hand, contagem in contagem_kraken_hand.items():
            post_detail.append(PostsDetail(
                kraken_hand=kraken_hand,
                post_count=contagem
            ))


        return GetPostByMonth(post_detail=post_detail, date=date)

    def post_clip_instagram(self, payload: PostInstagramClip):
        if payload.schedule:
            payload.schedule = payload.schedule + timedelta(hours=3)
        kraken_model, kraken_clips = self.create_kraken_and_clips(payload.clip_name,
                                                    payload.clip_id,
                                                    payload.url,
                                                    payload.caption,
                                                    KrakenHand.INSTAGRAM.value,
                                                    payload.kraken_head.value,
                                                    payload.id,
                                                    payload.schedule)
        payload = dict(payload)
        payload['kraken_id'] = kraken_model.id
        payload['kraken_head'] = kraken_clips.kraken_head

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
        kraken_model, kraken_clips = self.create_kraken_and_clips(payload.clip_name,
                                                    payload.clip_id,
                                                    payload.url,
                                                    payload.caption,
                                                    KrakenHand.TWITTER.value,
                                                    payload.kraken_head.value,
                                                    payload.id,
                                                    payload.schedule)

        payload = dict(payload)
        payload['kraken_id'] = kraken_model.id
        payload['kraken_head'] = kraken_clips.kraken_head

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
                                schedule: datetime = None):
        if id:
            kraken_clips = self.kraken_clips_repo.get_clips_by_id(id)
        else:
            kraken_clips_model = KrakenClips(
                clip_name=clip_name,
                clip_id=clip_id,
                clip_url=url,
                kraken_head=kraken_head
            )

            kraken_clips = self.kraken_clips_repo.add(kraken_clips_model)

        kraken_model = Kraken(
            post_status=PostStatus.CREATED.value,
            kraken_hand=kraken_hand,
            kraken_clips_id=kraken_clips.id,
            caption=caption,
            schedule=schedule
        )

        self.kraken_repo.add(kraken_model)

        return kraken_model, kraken_clips

    def get_clip_data(self, id: int) -> PostInstagramClip:
        kraken_clip = self.kraken_clips_repo.get_clips_by_id(id)
        response = PostInstagramClip(
            id=kraken_clip.id,
            url=kraken_clip.clip_url,
            caption=kraken_clip.kraken[0].caption,
            clip_id=kraken_clip.clip_id,
            clip_name=kraken_clip.clip_name,
            schedule=kraken_clip.kraken[0].schedule,
            kraken_head=kraken_clip.kraken_head
        )

        return response

    def post_clip_tiktok(self, payload):
        if payload.schedule:
            payload.schedule = payload.schedule + timedelta(hours=3)
        kraken_model, kraken_clips = self.create_kraken_and_clips(payload.clip_name,
                                                    payload.clip_id,
                                                    payload.url,
                                                    payload.caption,
                                                    KrakenHand.TIKTOK.value,
                                                    payload.kraken_head.value,
                                                    payload.id,
                                                    payload.schedule)
        payload = dict(payload)
        payload['kraken_id'] = kraken_model.id
        payload['kraken_head'] = kraken_clips.kraken_head

        if payload['schedule']:
            tasks.post_tiktok.apply_async(
                args=[dict(payload)], connect_timeout=10, eta=payload['schedule']
            )
        else:
            tasks.post_tiktok.apply_async(
                args=[dict(payload)], connect_timeout=10
            )

    def update_status(self, post_change_status: PostChangeStatus):
        kraken_model = Kraken(
            id=post_change_status.id,
            post_status=post_change_status.post_status.value,
            kraken_hand=KrakenHand.TIKTOK
            )
        return self.kraken_repo.update_status(kraken_model)
