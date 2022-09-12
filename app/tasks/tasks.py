import os
import time

from app.config.logger import Logger
from app.db.repositories.instagram_tasks_repository import InstagramTasksRepository
from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.db.repositories.parameters_repository import ParametersRepository
from app.db.repositories.reddit_send_message_repository import RedditSendMessageRepository
from app.db.repositories.reddit_tasks_repository import RedditTasksRepository
from app.integrations.Instagram_bot_integration import InstagramBotIntegration
from app.integrations.reddit_integration import RedditIntegration
from app.integrations.twitch_integration import TwitchIntegration
from app.integrations.twitter_integration import TwitterIntegration
from app.integrations.youtube_integration import YoutubeIntegration
from app.models.entities import Kraken, TwitterSendMessage, KrakenClips
from app.models.entities.reddit_send_message import RedditSendMessage
from app.models.schemas.kraken import PostStatus, KrakenHead
from app.services.clients.s3 import S3Service
from app.services.instagram_service import InstagramServices
from app.services.tiktok_service import TiktokServices
from app.tasks.base import DatabaseTask

from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitter_send_message_repository import (
    TwitterSendMessageRepository,
)
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.tasks.reddit_task.tools import get_reddit_users_to_send, get_reddit_send_message_params

from celery_app import app


logging = Logger.get_logger("Tasks")


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_twitter(self, payload):
    kraken_model = Kraken(id=payload["kraken_id"])
    try:
        clip_path = None
        logging.info("Processo de postar no twitter")
        if payload["kraken_head"] == KrakenHead.YOUTUBE.value:
            logging.info("Baixando do Youtube")
            change_status(self, kraken_model, PostStatus.DOWNLOADING_CLIP.value)
            clip_path = download_clip_youtube(payload["url"])
        elif payload["kraken_head"] == KrakenHead.TWITCH.value:
            logging.info("Baixando da Twitch")
            change_status(self, kraken_model, PostStatus.DOWNLOADING_CLIP.value)
            clip_path = download_clip_twitch(payload["url"])

        twitter_tasks_repo = TwitterTasksRepository(self.get_db)
        twitter_info = twitter_tasks_repo.get_task_by_twitter_handle(payload['twitter_handle'])

        twitter_integration = TwitterIntegration(
            consumer_key=twitter_info.consumer_key,
            consumer_secret=twitter_info.consumer_secret,
            oauth_secret=twitter_info.oauth_secret,
            oauth_token=twitter_info.oauth_token
        )

        is_posted = twitter_integration.post_media(clip_path, payload['caption'])
        os.remove(clip_path)

        if not is_posted:
            logging.info("Não foi possível postar.")
            change_status(self, kraken_model, PostStatus.ERROR.value)
        else:
            logging.info("Postado!")
            change_status(self, kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        change_status(self, kraken_model, PostStatus.ERROR.value)


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_instagram(self, payload):
    kraken_model = Kraken(id=payload["kraken_id"])
    try:
        change_status(self, kraken_model, PostStatus.INITIATED.value)
        logging.info("Processo de postar no instagram")
        url = None
        if payload["kraken_head"] == KrakenHead.YOUTUBE.value:
            url = payload['url'].replace('//app', '/%2Fapp')
        if payload["kraken_head"] == KrakenHead.TWITCH.value:
            url = payload['url'].split("-preview", 1)[0] + ".mp4"
        if not url:
            raise Exception("Url não localizada")
        change_status(self, kraken_model, PostStatus.POSTING.value)
        instagram_services = InstagramServices()
        logging.info("Processo de postagem iniciado")
        is_posted = instagram_services.post_clip(payload["caption"], url)
        if not is_posted:
            logging.info("Não foi possível postar.")
            change_status(self, kraken_model, PostStatus.ERROR.value)
        else:
            logging.info("Postado!")
            change_status(self, kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        logging.info(f"Erro ao postar: {ex}")
        change_status(self, kraken_model, PostStatus.ERROR.value)
        raise Exception(f"{ex}")


def download_clip_twitch(url: str) -> str:
    twitch_integration = TwitchIntegration()
    return twitch_integration.download_clip(url)


def download_clip_youtube(url: str) -> str:
    s3 = S3Service()
    return s3.download_file_url(url)


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def instagram_follow(self):
    users_per_round_instagram = 20
    total_geral_instagram = 7500
    sleep_per_follow_instagram = 60
    follow_per_round_instagram = 8

    instagram_tasks_repo = InstagramTasksRepository(self.get_db)
    tasks_follow = instagram_tasks_repo.get_tasks()
    parameter_repo = ParametersRepository(self.get_db)

    parameters = parameter_repo.get_parameters()
    for parameter in parameters:
        if parameter.name == "users_per_round_instagram":
            users_per_round_instagram = parameter.int_value
        elif parameter.name == "total_geral_instagram":
            total_geral_instagram = parameter.int_value
        elif parameter.name == "sleep_per_follow_instagram":
            sleep_per_follow_instagram = parameter.int_value
        elif parameter.name == "follow_per_round_instagram":
            follow_per_round_instagram = parameter.int_value

    for task in tasks_follow:
        if task.instagram_follow is not None:
            logging.info(
                f"Começando processo para o instagram {task.instagram_follow.instagram_handle}"
            )
            instagram_integration = InstagramBotIntegration(
                task.username, task.password
            )
            followings = instagram_integration.get_followers()
            if len(followings) >= total_geral_instagram:
                logging.error("Não roda mais")
                break
            users_to_follow = []
            users_followed = 0
            logging.info("Começando processo de buscar os usuários")
            for tag in task.instagram_follow.tag.split("|"):
                users_by_tag = instagram_integration.get_users_by_tag(tag)
                logging.info(
                    f"Usuários buscados na request: {len(users_by_tag)} na tag {tag}"
                )
                for user in users_by_tag:
                    if int(user["pk"]) not in followings:
                        if len(users_to_follow) >= users_per_round_instagram:
                            break
                        users_to_follow.append(user["pk"])
                logging.info(f"Usuários localizados: {len(users_to_follow)}")
                if len(users_to_follow) >= users_per_round_instagram:
                    break

            logging.info(f"Localizado: {len(users_to_follow)} usuários para seguir.")

            for user_id in users_to_follow:
                if users_followed == follow_per_round_instagram:
                    break
                try:
                    followed = instagram_integration.follow_user(user_id)
                    if followed:
                        logging.info(f"usuário: {user_id} seguido!")
                        users_followed += 1
                        time.sleep(sleep_per_follow_instagram)
                    else:
                        logging.info(f"Usuário: {user_id} não seguido.")
                except Exception as ex:
                    logging.info(f"Usuário não seguido: {ex}")


def get_send_message_params(parameter_repo):
    messages_per_hour = 25
    sleep_per_send = 100
    users_per_round = 50

    parameters = parameter_repo.get_parameters()
    for parameter in parameters:
        if parameter.name == "messages_per_hour":
            messages_per_hour = parameter.int_value
        elif parameter.name == "sleep_per_send":
            sleep_per_send = parameter.int_value
        elif parameter.name == "users_per_round":
            users_per_round = parameter.int_value

    return messages_per_hour, sleep_per_send, users_per_round


def get_users_to_send(
    tags,
    twitter_integration,
    result_type,
    stored_users_ids,
    users_per_round,
    parameter_repo,
    trending_user,
):
    users_to_send = []
    for tag in tags:
        users_by_tag = twitter_integration.search_tweets(q=tag, result_type=result_type)
        for user in users_by_tag:
            if (
                int(user.user.id) not in stored_users_ids
                and int(user.user.id) not in users_to_send
            ):
                users_to_send.append(user.user.id)
        if len(users_to_send) >= users_per_round:
            break

    if trending_user and len(users_to_send) < users_per_round:
        trends = twitter_integration.get_trending()
        trends_names = [x["name"] for x in trends]
        trends_filtered = twitter_integration.filter_trends(
            trends_names, parameter_repo
        )
        for tag in trends_filtered:
            users_by_tag = twitter_integration.search_tweets(
                q=tag, result_type=result_type
            )
            for user in users_by_tag:
                if (
                    int(user.user.id) not in stored_users_ids
                    and int(user.user.id) not in users_to_send
                ):
                    users_to_send.append(user.user.id)
            if len(users_to_send) >= users_per_round:
                break

    return users_to_send


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def twitter_follow(self):
    users_per_round = 50
    total_geral = 5000
    sleep_per_follow = 60
    follow_per_round = 30

    twitter_tasks_repo = TwitterTasksRepository(self.get_db)
    tasks_follow = twitter_tasks_repo.get_tasks()
    parameter_repo = ParametersRepository(self.get_db)

    parameters = parameter_repo.get_parameters()
    for parameter in parameters:
        if parameter.name == "users_per_round":
            users_per_round = parameter.int_value
        elif parameter.name == "total_geral":
            total_geral = parameter.int_value
        elif parameter.name == "sleep_per_follow":
            sleep_per_follow = parameter.int_value
        elif parameter.name == "follow_per_round":
            follow_per_round = parameter.int_value

    for task in tasks_follow:
        if task.twitter_follow is not None:
            logging.info(
                f"Começando processo para o twitter handle {task.twitter_follow.twitter_handle}"
            )
            twitter_integration = TwitterIntegration(
                task.consumer_key,
                task.consumer_secret,
                task.oauth_token,
                task.oauth_secret,
            )
            followings = twitter_integration.get_followers()
            if len(followings) >= total_geral:
                logging.info("Não roda mais")
                break

            users_to_follow = get_users_to_send(
                            task.twitter_follow.tag.split("|"),
                            twitter_integration,
                            task.twitter_follow.result_type,
                            followings,
                            users_per_round,
                            parameter_repo,
                            task.is_trending_user)

            logging.info(f"Localizado: {len(users_to_follow)} usuários para o seguir.")
            users_followed = 0
            for user_id in users_to_follow:
                if users_followed == follow_per_round:
                    break
                try:
                    twitter_integration.follow_user(user_id)
                    users_followed += 1
                    time.sleep(sleep_per_follow)
                except Exception as ex:
                    if ex.api_codes[0] == 161:
                        break


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def twitter_send_message(self):
    twitter_repository = TwitterSendMessageRepository(self.get_db)
    twitter_tasks_repo = TwitterTasksRepository(self.get_db)
    tasks_send_message = twitter_tasks_repo.get_tasks()
    parameter_repo = ParametersRepository(self.get_db)

    messages_per_hour, sleep_per_send, users_per_round = get_send_message_params(
        parameter_repo
    )

    for task in tasks_send_message:
        twitter_handle = task.twitter_handle
        if task.use_same_db:
            twitter_handle = task.use_same_db_twitter_handle

        twitter_integration = TwitterIntegration(
            task.consumer_key, task.consumer_secret, task.oauth_token, task.oauth_secret
        )

        stored_users = twitter_repository.get_users_by_twitter_handle(twitter_handle)
        stored_users_ids = [x.user_id for x in stored_users]
        sended_users = []
        logging.info(f"Twitter: {task.twitter_handle}")
        logging.info(f"Usuários já enviados: {len(stored_users_ids)}")

        users_to_send = get_users_to_send(
            task.twitter_messages.tag.split("|"),
            twitter_integration,
            task.twitter_messages.result_type,
            stored_users_ids,
            users_per_round,
            parameter_repo,
            task.is_trending_user,
        )
        logging.info(f"Localizado: {len(users_to_send)} usuários para o envio.")
        sended_count = 0
        not_sended_count = 0
        for user_id in users_to_send:
            if len(sended_users) == messages_per_hour:
                break

            sended = twitter_integration.send_message(
                task.twitter_messages.message, user_id
            )
            twitter_orm = TwitterSendMessage(
                user_id=user_id, sended=True, twitter_handle=twitter_handle
            )
            if sended:
                sended_users.append(user_id)
                twitter_repository.add(twitter_orm)
                time.sleep(sleep_per_send)
                sended_count += 1
            else:
                twitter_orm.sended = False
                twitter_repository.add(twitter_orm)
                not_sended_count += 1

        logging.info(
            f"Mensagens enviados: {str(sended_count)}, Mensagens não enviadas: {str(not_sended_count)}"
        )


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def reddit_get_users(self):
    reddit_repository = RedditSendMessageRepository(self.get_db)
    reddit_tasks_repo = RedditTasksRepository(self.get_db)
    tasks_send_message = reddit_tasks_repo.get_tasks()
    for task in tasks_send_message:
        reddit_integration = RedditIntegration(
            task.client_id, task.client_secret, task.username, task.password
        )

        stored_users = reddit_repository.get_users_by_reddit_handle(task.reddit_handle)
        stored_users_ids = [x.user_id for x in stored_users]
        logging.info(f"Reddit: {task.reddit_handle}")

        users_to_send = get_reddit_users_to_send(
            task.reddit_messages.tag.split("|"),
            reddit_integration,
            stored_users_ids,
            50
        )

        for user in users_to_send:
            reddit_orm = RedditSendMessage(
                user_id=user, sended=False, reddit_handle=task.reddit_handle
            )
            reddit_repository.add(reddit_orm)


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def reddit_send_message(self):
    reddit_repository = RedditSendMessageRepository(self.get_db)
    reddit_tasks_repo = RedditTasksRepository(self.get_db)
    tasks_send_message = reddit_tasks_repo.get_tasks()
    parameter_repo = ParametersRepository(self.get_db)

    messages_per_hour, sleep_per_send, users_per_round = get_reddit_send_message_params(
        parameter_repo
    )

    for task in tasks_send_message:
        reddit_integration = RedditIntegration(
            task.client_id, task.client_secret, task.username, task.password
        )

        stored_users = reddit_repository.get_users_by_reddit_handle(task.reddit_handle)
        stored_users_ids = [x.user_id for x in stored_users]
        sended_users = []
        logging.info(f"Reddit: {task.reddit_handle}")
        logging.info(f"Reddit: Usuários já enviados: {len(stored_users_ids)}")

        users_to_send = reddit_repository.get_users_by_reddit_handle(task.reddit_handle, False)
        logging.info(f"Reddit: Localizado: {len(users_to_send)} usuários para o envio.")
        sended_count = 0
        not_sended_count = 0
        for user in users_to_send:
            if len(sended_users) == messages_per_hour:
                break

            sended = reddit_integration.send_message(
                user.user_id, task.reddit_messages.message
            )
            if sended:
                reddit_repository.update_sended(user.id, True)
                sended_users.append(user.id)
                time.sleep(sleep_per_send)
                sended_count += 1
            else:
                not_sended_count += 1

        logging.info(
            f"Reddit: Mensagens enviados: {str(sended_count)}, Mensagens não enviadas: {str(not_sended_count)}"
        )


def change_status(self, kraken_model, new_status):
    kraken_repository = KrakenRepository(self.get_db)
    kraken_model.post_status = new_status
    kraken_repository.update_status(kraken_model)


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def cut_youtube_video(self, payload):
    kraken_clips_repo = KrakenClipsRepository(self.get_db)
    youtube_integration = YoutubeIntegration()

    try:
        video_path = youtube_integration.download_video(payload["video_url"])
        clip_s3_url, thumbnail = youtube_integration.custom_crop(
            video_path, payload["start"], payload["end"]
        )

        youtube_clip = KrakenClips(
            clip_name=payload["caption"],
            clip_id=payload["youtube_id"],
            clip_url=clip_s3_url,
            thumbnail=thumbnail,
            kraken_head='YOUTUBE'
        )

        kraken_clips_repo.add(youtube_clip)
    except Exception as ex:
        logging.info(f"Erro ao criar clip: {ex}")


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def post_tiktok(self, payload):
    kraken_model = Kraken(id=payload["kraken_id"])
    try:
        change_status(self, kraken_model, PostStatus.INITIATED.value)
        logging.info("Processo de postar no instagram")
        url = None
        if payload["kraken_head"] == KrakenHead.YOUTUBE.value:
            url = payload['url'].replace('//app', '/%2Fapp')
        if payload["kraken_head"] == KrakenHead.TWITCH.value:
            url = payload['url'].split("-preview", 1)[0] + ".mp4"
        if not url:
            raise Exception("Url não localizada")
        change_status(self, kraken_model, PostStatus.POSTING.value)
        tiktok_services = TiktokServices()
        logging.info("Processo de postagem iniciado")
        is_posted = tiktok_services.post_clip(payload["caption"], url)
        if not is_posted:
            logging.info("Não foi possível postar.")
            change_status(self, kraken_model, PostStatus.ERROR.value)
        else:
            logging.info("Postado!")
            change_status(self, kraken_model, PostStatus.COMPLETED.value)
    except Exception as ex:
        logging.info(f"Erro ao postar: {ex}")
        change_status(self, kraken_model, PostStatus.ERROR.value)
        raise Exception(f"{ex}")


@app.task(bind=True, max_retries=5, base=DatabaseTask)
def create_twitch_clips(self):
    kraken_clips_repo = KrakenClipsRepository(self.get_db)
    clips = self.twitch_integration.get_all_clips(first=100)
    all_clips = [x for x in clips['data']]
    while clips['pagination'].get('cursor'):
        last_cursor = clips['pagination']['cursor']
        clips = self.twitch_integration.get_all_clips(after_cursor=last_cursor, first=100)
        [all_clips.append(x) for x in clips['data']]

    add_clips = []
    if len(all_clips) > 0:
        for new_clip in all_clips:
            kraken_clips_model = KrakenClips(
                created_at=new_clip['created_at'],
                clip_name=new_clip['title'],
                clip_id=new_clip['id'],
                clip_url=new_clip['thumbnail_url'],
                thumbnail=new_clip['thumbnail_url']
            )
            add_clips.append(kraken_clips_model)

    for new_clip in add_clips:
        clip_stored = kraken_clips_repo.get_clips_by_clip_id(new_clip.clip_id)
        if not clip_stored:
            kraken_clips_repo.add(new_clip)