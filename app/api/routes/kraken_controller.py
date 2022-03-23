from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.kraken import get_twitch_service, get_kraken_service
from app.models.schemas.kraken import TwitchClipsResponse, PostInstagramClip, PostQueue, TwitchClipsResponsePagination
from app.services.kraken_services import KrakenServices
from app.services.twitch_service import TwitchServices

router = APIRouter()


@router.get(
    "/get_twitch_clips",
    name="Kraken: Get twitch clips by broadcaster",
    status_code=200,
    response_model=TwitchClipsResponsePagination
)
def get_twitch_clips(next_cursor: str = None, back_cursor: str = None, twitch_service: TwitchServices = Depends(get_twitch_service)):
    clips = twitch_service.get_clips(next_cursor=next_cursor, back_cursor=back_cursor)
    return clips


@router.post(
    "/post_instagram_clip",
    name="Kraken: Queue instagram twitch clip",
    status_code=201
)
async def post_clip_instagram(payload: PostInstagramClip, twitch_service: TwitchServices = Depends(get_twitch_service)):
    await twitch_service.post_clip_instagram(payload)


@router.get(
    "/get_posts_queue",
    name="Kraken: Get posts queue",
    status_code=200,
    response_model=List[PostQueue]
)
async def get_posts_queue(kraken_service: KrakenServices = Depends(get_kraken_service)):
    queue_posts = await kraken_service.get_posts_queue_async()
    return queue_posts
