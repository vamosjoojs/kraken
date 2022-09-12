from fastapi import APIRouter, Depends

from app.api.dependencies.fetch_params import FetchParams
from app.api.dependencies.kraken import get_twitch_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import TwitchClipsResponse
from app.services.twitch_service import TwitchServices

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
