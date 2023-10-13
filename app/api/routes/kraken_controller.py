import datetime

from fastapi import APIRouter, Depends

from app.api.dependencies.fetch_params import FetchParams
from app.api.dependencies.kraken import get_kraken_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import PostQueue, PostInstagramClip, PostTwitterClip, PostTiktokClip, PostChangeStatus, \
    GetPostByMonth, PostStatus
from app.services.kraken_services import KrakenServices

router = APIRouter()


@router.get(
    "/get_posts_queue",
    name="Kraken: Get posts queue",
    status_code=200,
    response_model=Paginated[PostQueue],
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_posts_queue(
        kraken_service: KrakenServices = Depends(get_kraken_service),
        common: FetchParams = Depends(),
):
    queue_posts = kraken_service.get_posts_queue_async(common.page, common.page_size)
    return queue_posts

@router.get(
    "/get_posts_by_date",
    name="Kraken: Get posts queue by date",
    status_code=200,
    response_model=GetPostByMonth,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_posts_queue_by_date(
        date: datetime.date,
        post_status: PostStatus,
        kraken_service: KrakenServices = Depends(get_kraken_service),
):
    queue_posts = kraken_service.get_posts_by_date(date, post_status)
    return queue_posts

@router.put(
    "/update_status",
    name="Kraken: update status",
    status_code=200,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_posts_queue(
    post_change_status: PostChangeStatus,
    kraken_service: KrakenServices = Depends(get_kraken_service),
):
    return kraken_service.update_status(post_change_status)


@router.get(
    "/get_clip_data",
    name="Kraken: Get clip data",
    status_code=200,
    response_model=PostInstagramClip,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_clip_data(
        id: int,
        kraken_service: KrakenServices = Depends(get_kraken_service),
):
    clip_data = kraken_service.get_clip_data(id)
    return clip_data


@router.post(
    "/post_instagram_clip",
    name="Kraken: Queue instagram twitch clip",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def post_clip_instagram(payload: PostInstagramClip, kraken_services: KrakenServices = Depends(get_kraken_service)):
    kraken_services.post_clip_instagram(payload)


@router.post(
    "/post_twitter_clip",
    name="Kraken: Post twitch clip in Twitter",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def post_clip_twitter(payload: PostTwitterClip, kraken_services: KrakenServices = Depends(get_kraken_service)):
    kraken_services.post_clip_twitter(payload)


@router.post(
    "/post_tiktok_clip",
    name="Kraken: Post clip in Tiktok",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def post_clip_tiktok(payload: PostTiktokClip, kraken_services: KrakenServices = Depends(get_kraken_service)):
    kraken_services.post_clip_tiktok(payload)
