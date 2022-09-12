from fastapi import APIRouter, Depends

from app.api.dependencies.fetch_params import FetchParams
from app.api.dependencies.kraken import get_twitch_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import TwitchClipsResponse
from app.services.twitch_service import TwitchServices
from app.tasks import tasks

router = APIRouter()


@router.get(
    "/get_twitch_clips",
    name="Kraken: Get twitch clips by broadcaster",
    status_code=200,
    response_model=Paginated[TwitchClipsResponse],
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_twitch_clips(twitch_service: TwitchServices = Depends(get_twitch_service), common: FetchParams = Depends()):
    clips = twitch_service.get_clips(page=common.page)
    return clips


@router.post(
    "/trigger_update_twitch_clips",
    name="Kraken: Update Twitch Clips",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def update_twitch_clips():
    tasks.create_twitch_clips.apply_async(connect_timeout=10)

