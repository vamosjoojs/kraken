import asyncio
import datetime
import os
import time

import requests

from app.integrations.twitch_integration import TwitchIntegration
from app.models.entities import Kraken
from app.models.schemas.kraken import PostStatus, PostInstagramClip
from app.services.instagram_service import InstagramServices
from app.tasks.base import DatabaseTask

from celery_app import app


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_instagram(self, payload):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_post_instagram(self, payload))


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def automatic_post_instagram(self, payload):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getclips(self, payload))


async def getclips(self, payload):
    while True:
        auto_tasks = await self.auto_tasks_repository.get_instagram_state_switch(payload['auto_task_id'])
        if auto_tasks is None:
            print("parando processo")
            break
        twitch_integration = TwitchIntegration()
        clips = twitch_integration.get_all_clips(start_at=datetime.datetime.utcnow(), first=99)
        for clip in clips['data']:
            if clip['creator_name'] == payload['creator_name']:
                print(f"Clip localizado {clip['title']}")
                post_instagram = PostInstagramClip(
                    thumbnail=clip['thumbnail_url'],
                    caption=payload['caption'],
                    clip_id=clip['id'],
                    clip_name=clip['title']
                )
                requests.post("http://localhost/api/twitch/post_instagram_clip", data=post_instagram)

        time.sleep(60)


async def change_status(self, kraken_model, new_status):
    kraken_model.post_status = new_status
    await self.kraken_repository.update_status(kraken_model)


async def async_post_instagram(self, payload):
    kraken_model = Kraken(id=payload['kraken_id'],
                          post_status=PostStatus.INITIATED.value)

    await self.kraken_repository.update_status(kraken_model)
    try:
        twitch_integration = TwitchIntegration()
        await change_status(self, kraken_model, PostStatus.DOWNLOADING_CLIP.value)
        clip_path = twitch_integration.download_clip(payload["thumbnail"])

        await change_status(self, kraken_model, PostStatus.POSTING.value)
        instagram_services = InstagramServices()
        instagram_services.post_clip(payload["caption"], clip_path)
        os.remove(clip_path)
        await change_status(self, kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        await change_status(self, kraken_model, PostStatus.ERROR.value)
        raise Exception(f"{ex}")
