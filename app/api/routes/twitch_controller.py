from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitch_service
from app.models.schemas.kraken import PostInstagramClip, TwitchClipsResponsePagination, AutomaticPostInstagramClip, \
    PostTwitterClip
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
def post_clip_instagram(payload: PostInstagramClip, twitch_service: TwitchServices = Depends(get_twitch_service)):
    twitch_service.post_clip_instagram(payload)


@router.post(
    "/test_selenium",
    name="Kraken: Queue instagram twitch clip",
    status_code=201
)
def teste(twitch_service: TwitchServices = Depends(get_twitch_service)):
    twitch_service.post_clip_instagram_manual()


@router.post(
    "/automatic_post_instagram_clip",
    name="Kraken: Automatic queue instagram twitch clip",
    status_code=201
)
def automatic_post_clip_instagram(payload: AutomaticPostInstagramClip, twitch_service: TwitchServices = Depends(get_twitch_service)):
    return twitch_service.automatic_post_clip_instagram(payload)


@router.put(
    "/disable_automatic_post_instagram_clip/{id}",
    name="Kraken: Disable automatic queue instagram twitch clip",
    status_code=200
)
def disable_automatic_post_clip_instagram(id: int, twitch_service: TwitchServices = Depends(get_twitch_service)):
    twitch_service.disable_automatic_post_clip_instagram(id)


@router.put(
    "/change_post_status",
    name="Kraken: Post status",
    status_code=200
)
def change_post_status(payload: AutomaticPostInstagramClip, twitch_service: TwitchServices = Depends(get_twitch_service)):
    twitch_service.automatic_post_clip_instagram(payload)


@router.post(
    "/post_twitter_clip",
    name="Kraken: Post twitch clip in Twitter",
    status_code=201
)
def post_clip_twitter(payload: PostTwitterClip, twitch_service: TwitchServices = Depends(get_twitch_service)):
    twitch_service.post_clip_twitter(payload)
