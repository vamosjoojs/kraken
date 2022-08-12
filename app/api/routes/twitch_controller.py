from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitch_service
from app.auth.auth_bearer import JWTBearer
from app.config import logger
from app.models.schemas.kraken import TwitchClipsResponsePagination
from app.services.twitch_service import TwitchServices

router = APIRouter()


@router.get(
    "/get_twitch_clips",
    name="Kraken: Get twitch clips by broadcaster",
    status_code=200,
    response_model=TwitchClipsResponsePagination,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_twitch_clips(next_cursor: str = None, back_cursor: str = None, twitch_service: TwitchServices = Depends(get_twitch_service)):
    clips = twitch_service.get_clips(next_cursor=next_cursor, back_cursor=back_cursor)
    return clips
