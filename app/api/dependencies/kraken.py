from fastapi.param_functions import Depends

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.repositories.twitter_tasks_repository import TwitterTasksRepository
from app.db.repositories.twitter_send_message_repository import TwitterSendMessageRepository
from app.db.uow import UnitOfWork
from sqlalchemy.orm import Session

from app.api.dependencies.get_db import get_uow

from app.db.repositories.twitch_repository import TwitchRepository
from app.services.instagram_service import InstagramServices
from app.services.kraken_services import KrakenServices
from app.services.twitch_service import TwitchServices
from app.services.twitter_service import TwitterServices


def get_twitch_service(session: Session = Depends(get_uow)) -> TwitchServices:
    uow = UnitOfWork(session)
    repository = TwitchRepository(uow)
    kraken_repository = KrakenRepository(uow)
    auto_tasks_repository = AutoTasksRepository(uow)

    return TwitchServices(repository, kraken_repository, auto_tasks_repository)


def get_instagram_service(
) -> InstagramServices:
    return InstagramServices()


def get_kraken_service(session: Session = Depends(get_uow)) -> KrakenServices:
    uow = UnitOfWork(session)
    repository = KrakenRepository(uow)
    return KrakenServices(repository)


def get_twitter_service(session: Session = Depends(get_uow)) -> TwitterServices:
    uow = UnitOfWork(session)
    auto_tasks_repository = AutoTasksRepository(uow)
    twitter_tasks = TwitterTasksRepository(uow)
    twitter_send_message = TwitterSendMessageRepository(uow)
    return TwitterServices(auto_tasks_repository, twitter_tasks, twitter_send_message)
