from fastapi.param_functions import Depends

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.instagram_tasks_repository import InstagramTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.parameters_repository import ParametersRepository
from app.db.repositories.reddit_send_message_repository import RedditSendMessageRepository
from app.db.repositories.reddit_tasks_repository import RedditTasksRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.db.repositories.twitter_send_message_repository import TwitterSendMessageRepository
from app.db.uow import UnitOfWork
from sqlalchemy.orm import Session

from app.api.dependencies.get_db import get_uow

from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.services.instagram_bot_service import InstagramBotServices
from app.services.instagram_service import InstagramServices
from app.services.kraken_services import KrakenServices
from app.services.parameters_services import ParametersServices
from app.services.reddit_service import RedditServices
from app.services.twitch_service import TwitchServices
from app.services.twitter_service import TwitterServices
from app.services.youtube_service import YoutubeServices


def get_twitch_service(session: Session = Depends(get_uow)) -> TwitchServices:
    uow = UnitOfWork(session)
    kraken_clips_repo = KrakenClipsRepository(uow)
    return TwitchServices(kraken_clips_repo)


def get_instagram_service(
) -> InstagramServices:
    return InstagramServices()


def get_instagram_bot_service(session: Session = Depends(get_uow)) -> InstagramBotServices:
    uow = UnitOfWork(session)
    repository = InstagramTasksRepository(uow)
    return InstagramBotServices(repository)


def get_kraken_service(session: Session = Depends(get_uow)) -> KrakenServices:
    uow = UnitOfWork(session)
    auto_tasks_repository = AutoTasksRepository(uow)
    repository = KrakenRepository(uow)
    kraken_clips_repo = KrakenClipsRepository(uow)
    twitter_tasks = TwitterTasksRepository(uow)
    return KrakenServices(repository, kraken_clips_repo, twitter_tasks, auto_tasks_repository)


def get_twitter_service(session: Session = Depends(get_uow)) -> TwitterServices:
    uow = UnitOfWork(session)
    auto_tasks_repository = AutoTasksRepository(uow)
    twitter_tasks = TwitterTasksRepository(uow)
    twitter_send_message = TwitterSendMessageRepository(uow)
    return TwitterServices(auto_tasks_repository, twitter_tasks, twitter_send_message)


def get_reddit_service(session: Session = Depends(get_uow)) -> RedditServices:
    uow = UnitOfWork(session)
    reddit_tasks = RedditTasksRepository(uow)
    reddit_send_message = RedditSendMessageRepository(uow)
    repository = ParametersRepository(uow)

    return RedditServices(reddit_tasks, reddit_send_message, repository)


def get_parameters_service(session: Session = Depends(get_uow)) -> ParametersServices:
    uow = UnitOfWork(session)
    repository = ParametersRepository(uow)
    return ParametersServices(repository)


def get_youtube_service(session: Session = Depends(get_uow)) -> YoutubeServices:
    uow = UnitOfWork(session)
    kraken_clips_repo = KrakenClipsRepository(uow)
    return YoutubeServices(kraken_clips_repo)

