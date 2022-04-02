import asyncio
import datetime
import os
import time
import requests
import logging

from app.integrations.twitch_integration import TwitchIntegration
from app.integrations.twitter_integration import TwitterIntegration
from app.models.entities import Kraken, TwitterSendMessage
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


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def twitter_send_message(self, payload):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(automatic_twitter_send_message(self, payload))


async def getclips(self, payload):
    while True:
        try:
            auto_tasks = await self.auto_tasks_repository.get_instagram_state_switch(payload['auto_task_id'])
            if auto_tasks is None:
                print("parando processo")
                break
            twitch_integration = TwitchIntegration()
            clips = twitch_integration.get_all_clips(start_at=datetime.datetime.fromisoformat(payload['initial_date']), first=99)
            for clip in clips['data']:
                clip_stored = await self.twitch_repository.get_twitch_clips_by_clip_id(clip['id'])
                if clip_stored is None and clip['creator_name'] == payload['creator_name']:
                    print(f"Clip localizado {clip['title']}")
                    post_instagram = PostInstagramClip(
                        thumbnail=clip['thumbnail_url'],
                        caption=payload['caption'],
                        clip_id=clip['id'],
                        clip_name=clip['title']
                    )
                    requests.post("https://kraken-application.herokuapp.com/api/twitch/post_instagram_clip", data=post_instagram.json())
                    print("Clips enfileirado")
        except Exception as ex:
            print(ex)
            raise ex
        time.sleep(60)


async def change_status(self, kraken_model, new_status):
    kraken_model.post_status = new_status
    await self.kraken_repository.update_status(kraken_model)


async def async_post_instagram(self, payload):
    kraken_model = Kraken(id=payload['kraken_id'])
    try:
        await change_status(self,kraken_model, PostStatus.INITIATED.value)
        twitch_integration = TwitchIntegration()
        await change_status(self,kraken_model, PostStatus.DOWNLOADING_CLIP.value)
        clip_path = twitch_integration.download_clip(payload["thumbnail"])

        await change_status(self,kraken_model, PostStatus.POSTING.value)
        instagram_services = InstagramServices()
        instagram_services.post_clip(payload["caption"], clip_path)
        os.remove(clip_path)
        await change_status(self,kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        await change_status(self,kraken_model, PostStatus.ERROR.value)
        raise Exception(f"{ex}")


async def automatic_twitter_send_message(self, payload):
    # busca por parametros os dados de envio
    messages_per_hour = 25
    sleep_per_send = 100
    # busca por parametros os dados de envio

    twitter_integration = TwitterIntegration(
        payload['consumer_key'],
        payload['consumer_secret'],
        payload['oauth_token'],
        payload['oauth_secret']
    )

    stored_users = await self.twitter_repository.get_users_by_twitter_handle(payload['twitter_handler'])
    stored_users_ids = [x.user_id for x in stored_users]
    sended_users = []
    users_to_send = []

    logging.info(f"Usuários já enviados: {len(stored_users_ids)}")

    logging.info("Começando processo de buscar os usuários")
    max_requests = 10
    count = 0
    while count <= max_requests:
        logging.info(f"Usuários localizados: {len(users_to_send)}")
        try:
            users_by_tag = twitter_integration.search_tweets(payload['tag'])
            logging.info(f"Usuários buscados na request: {len(users_by_tag)}")
            for user in users_by_tag:
                if int(user.user.id) not in stored_users_ids and int(user.user.id) not in users_to_send:
                    users_to_send.append(user.user.id)
            count += 1
        except Exception as ex:
            logging.error(ex)
            raise ex

    logging.info(f"Localizado: {len(users_to_send)} usuários para o envio.")

    for user_id in users_to_send:
        if len(sended_users) == messages_per_hour:
            break

        sended = twitter_integration.send_message(payload['message'], user_id)
        logging.info(f"Mensagem enviada para {user_id}")
        twitter_orm = TwitterSendMessage(
            user_id=user_id,
            sended=True,
            twitter_handle=payload['twitter_handler']
        )
        if sended:
            sended_users.append(user_id)
            await self.twitter_repository.add(twitter_orm)
            time.sleep(sleep_per_send)
        else:
            twitter_orm.sended = False
            await self.twitter_repository.add(twitter_orm)
