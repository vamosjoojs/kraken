from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitch_service
from app.models.schemas.kraken import PostInstagramClip, TwitchClipsResponsePagination, AutomaticPostInstagramClip
from app.services.twitch_service import TwitchServices
from app.tasks import tasks

router = APIRouter()

#
# @router.get(
#     "/get_twitch_clips",
#     name="Kraken: Get twitch clips by broadcaster",
#     status_code=200,
#     response_model=TwitchClipsResponsePagination
# )
# def get_twitch_clips(next_cursor: str = None, back_cursor: str = None, twitch_service: TwitchServices = Depends(get_twitch_service)):
#     clips = twitch_service.get_clips(next_cursor=next_cursor, back_cursor=back_cursor)
#     return clips


@router.post(
    "/teste",
    name="Kraken: Queue instagram twitch clip",
    status_code=201
)
async def teste():
    tasks.twitter_send_message.apply_async(connect_timeout=10)
