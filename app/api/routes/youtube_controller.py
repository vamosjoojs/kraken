from fastapi import APIRouter, Depends

from app.api.dependencies.fetch_params import FetchParams
from app.api.dependencies.kraken import get_youtube_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import YoutubeClipsResponsePagination, CutVideoYoutube, YoutubeClipsResponse
from app.services.youtube_service import YoutubeServices

router = APIRouter()


@router.get(
    "/get_youtube_videos",
    name="Kraken: Get youtube videos",
    status_code=200,
    response_model=YoutubeClipsResponsePagination,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_youtube_videos(next_cursor: str = None, youtube_service: YoutubeServices = Depends(get_youtube_service)):
    clips = youtube_service.get_videos(next_cursor)
    return clips


@router.post(
    "/cut_video",
    name="Kraken: Cut video",
    status_code=200,
    response_model=str,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def cut_video(payload: CutVideoYoutube, youtube_service: YoutubeServices = Depends(get_youtube_service)):
    return youtube_service.crop_videos(payload.video_url,
                                       payload.start,
                                       payload.end,
                                       payload.caption,
                                       payload.youtube_id)


@router.get(
    "/get_youtube_clips",
    name="Kraken: Get youtube clips",
    status_code=200,
    response_model=YoutubeClipsResponsePagination,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_youtube_clips(youtube_id: str = None, youtube_service: YoutubeServices = Depends(get_youtube_service)):
    clips = youtube_service.get_clips(youtube_id)
    return clips


@router.get(
    "/get_all_youtube_clips",
    name="Kraken: Get all youtube clips",
    status_code=200,
    response_model=Paginated[YoutubeClipsResponse],
    dependencies=[Depends(JWTBearer(role="user"))],
)
def get_all_youtube_clips(youtube_service: YoutubeServices = Depends(get_youtube_service), common: FetchParams = Depends()):
    clips = youtube_service.get_all_clips(common.page)
    return clips
