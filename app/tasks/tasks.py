import asyncio
import os

from app.models.entities import Twitch
from app.models.schemas.kraken import PostStatus, KrakenHand
from app.services.instagram_service import InstagramServices
from app.services.twitch_service import TwitchIntegration
from app.tasks.base import DatabaseTask


from celery_app import app


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_instagram(self, payload):
    print("task recebida!!!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_post_instagram(self, payload))


async def async_post_instagram(self, payload):
    twitch_model = Twitch(id=payload['id'],
                          post_status=PostStatus.INITIATED.value,
                          kraken_hand=KrakenHand.INSTAGRAM.value,
                          clip_url=payload['thumbnail'])

    await self.twitch_repository.insert_or_update(twitch_model)
    try:
        twitch_integration = TwitchIntegration()
        twitch_model.post_status = PostStatus.DOWNLOADING_CLIP.value
        await self.twitch_repository.insert_or_update(twitch_model)
        clip_path = twitch_integration.download_clip(payload["thumbnail"])

        twitch_model.post_status = PostStatus.POSTING.value
        await self.twitch_repository.insert_or_update(twitch_model)
        instagram_services = InstagramServices()
        instagram_services.post_clip(payload.caption, clip_path)

        os.remove(clip_path)

        twitch_model.post_status = PostStatus.COMPLETED.value
        await self.twitch_repository.insert_or_update(twitch_model)
    except Exception:
        twitch_model.post_status = PostStatus.ERROR.value
        await self.twitch_repository.insert_or_update(twitch_model)
