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

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitch_repository import TwitchRepository
from app.db.repositories.twitter_send_message_repository import TwitterSendMessageRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository

from celery_app import app


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_instagram(self, payload):
    kraken_model = Kraken(id=payload['kraken_id'])
    try:
        change_status(self, kraken_model, PostStatus.INITIATED.value)
        twitch_integration = TwitchIntegration()
        change_status(self, kraken_model, PostStatus.DOWNLOADING_CLIP.value)
        clip_path = twitch_integration.download_clip(payload["thumbnail"])

        change_status(self, kraken_model, PostStatus.POSTING.value)
        instagram_services = InstagramServices()
        is_posted = instagram_services.post_clip(payload["caption"], clip_path)
        os.remove(clip_path)
        if not is_posted:
            change_status(self, kraken_model, PostStatus.ERROR.value)
        else:
            change_status(self, kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        change_status(self, kraken_model, PostStatus.ERROR.value)
        raise Exception(f"{ex}")


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def automatic_post_instagram(self, payload):
    auto_tasks_repository = AutoTasksRepository(self.get_db)
    twitch_repository = TwitchRepository(self.get_db)
    while True:
        try:
            auto_tasks = auto_tasks_repository.get_instagram_state_switch(payload['auto_task_id'])
            if auto_tasks is None:
                print("parando processo")
                break
            twitch_integration = TwitchIntegration()
            clips = twitch_integration.get_all_clips(start_at=datetime.datetime.fromisoformat(payload['initial_date']),
                                                     first=99)
            for clip in clips['data']:
                clip_stored = twitch_repository.get_twitch_clips_by_clip_id(clip['id'])
                if clip_stored is None and clip['creator_name'] == payload['creator_name']:
                    print(f"Clip localizado {clip['title']}")
                    post_instagram = PostInstagramClip(
                        thumbnail=clip['thumbnail_url'],
                        caption=payload['caption'],
                        clip_id=clip['id'],
                        clip_name=clip['title']
                    )
                    requests.post("https://kraken-application.herokuapp.com/api/twitch/post_instagram_clip",
                                  data=post_instagram.json())
                    print("Clips enfileirado")
        except Exception as ex:
            print(ex)
            raise ex
        time.sleep(60)


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def twitter_send_message(self, task):
    # busca por parametros os dados de envio
    messages_per_hour = 25
    sleep_per_send = 100
    users_per_round = 50
    # busca por parametros os dados de envio

    twitter_repository = TwitterSendMessageRepository(self.get_db)

    if task['use_same_db']:
        task['twitter_handle'] = task['use_same_db_twitter_handle']

    twitter_integration = TwitterIntegration(
        task['consumer_key'],
        task['consumer_secret'],
        task['oauth_token'],
        task['oauth_secret']
    )

    stored_users = twitter_repository.get_users_by_twitter_handle(task['twitter_handle'])
    stored_users_ids = [x.user_id for x in stored_users]
    sended_users = []
    users_to_send = []

    logging.info(f"Usuários já enviados: {len(stored_users_ids)}")
    logging.info("Começando processo de buscar os usuários")
    for tag in task['tag'].split('|'):
        users_by_tag = twitter_integration.search_tweets(tag)
        logging.info(f"Usuários buscados na request: {len(users_by_tag)} na tag {tag}")
        for user in users_by_tag:
            if int(user.user.id) not in stored_users_ids and int(user.user.id) not in users_to_send:
                users_to_send.append(user.user.id)
        logging.info(f"Usuários localizados: {len(users_to_send)}")
        if len(users_to_send) <= users_per_round:
            break

    logging.info(f"Localizado: {len(users_to_send)} usuários para o envio.")

    for user_id in users_to_send:
        if len(sended_users) == messages_per_hour:
            break

        sended = twitter_integration.send_message(task['message'], user_id)
        logging.info(f"Mensagem enviada para {user_id}")
        twitter_orm = TwitterSendMessage(
            user_id=user_id,
            sended=True,
            twitter_handle=task['twitter_handler']
        )
        if sended:
            sended_users.append(user_id)
            twitter_repository.add(twitter_orm)
            time.sleep(sleep_per_send)
        else:
            twitter_orm.sended = False
            twitter_repository.add(twitter_orm)


def change_status(self, kraken_model, new_status):
    kraken_repository = KrakenRepository(self.get_db)
    kraken_model.post_status = new_status
    kraken_repository.update_status(kraken_model)
