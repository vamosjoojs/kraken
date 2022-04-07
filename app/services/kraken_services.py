from typing import List

from app.db.repositories.kraken_repository import KrakenRepository
from app.models.schemas.kraken import PostQueue, PostStatus, KrakenHand


class KrakenServices:
    def __init__(self, kraken_repo: KrakenRepository):
        self.kraken_repo = kraken_repo

    def get_posts_queue_async(self) -> List[PostQueue]:
        queue_clips = self.kraken_repo.get_queue_posts()

        result_list = []
        for queue_clip in queue_clips:
            post_queue = PostQueue(
                created_at=queue_clip.created_at,
                post_status=PostStatus[queue_clip.post_status],
                kraken_hand=KrakenHand[queue_clip.kraken_hand],
                name=queue_clip.twitch_clips.clip_name
            )
            result_list.append(post_queue)

        return result_list

