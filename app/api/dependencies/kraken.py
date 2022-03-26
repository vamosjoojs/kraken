from fastapi.param_functions import Depends

from app.db.repositories.auto_tasks_repository import AutoTasksRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.db.uow import UnitOfWork
from app.api.dependencies.get_db import get_uow
from app.db.repositories.twitch_repository import TwitchRepository
from app.services.instagram_service import InstagramServices
from app.services.kraken_services import KrakenServices
from app.services.twitch_service import TwitchServices


async def get_twitch_service(
    uow: UnitOfWork = Depends(get_uow)
) -> TwitchServices:
    repository = TwitchRepository(uow)
    kraken_repository = KrakenRepository(uow)
    auto_tasks_repository = AutoTasksRepository(uow)

    return TwitchServices(repository, kraken_repository, auto_tasks_repository)


async def get_instagram_service(
) -> InstagramServices:
    return InstagramServices()


async def get_kraken_service(
    uow: UnitOfWork = Depends(get_uow)
) -> KrakenServices:
    repository = KrakenRepository(uow)
    return KrakenServices(repository)

