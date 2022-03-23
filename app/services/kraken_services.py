from typing import List

from app.db.repositories.twitch_repository import TwitchRepository
from app.models.schemas.kraken import PostQueue, PostStatus, KrakenHand


class KrakenServices:
    def __init__(self, twitch_repo: TwitchRepository):
        self.twitch_repo = twitch_repo

    async def get_posts_queue_async(self) -> List[PostQueue]:
        queue_clips = await self.twitch_repo.get_queue_twitch_posts()

        result_list = []
        for queue_clip in queue_clips:
            post_queue = PostQueue(
                created_at=queue_clip.created_at,
                post_status=PostStatus[queue_clip.post_status],
                kraken_hand=KrakenHand[queue_clip.kraken_hand]
            )
            result_list.append(post_queue)

        return result_list

