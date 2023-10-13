from fastapi import APIRouter, Depends, Request

from app.api.dependencies.kraken import get_tiktok_service
from app.auth.auth_bearer import JWTBearer
from app.services.tiktok_service import TiktokServices

router = APIRouter()


@router.post(
    "/refresh_token",
    name="Kraken: Tiktok auth",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def refresh_token(tiktok_service: TiktokServices = Depends(get_tiktok_service)):
    return tiktok_service.refresh_token()


@router.post(
    "/post_media",
    name="Kraken: Tiktok post",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def post_media(tiktok_service: TiktokServices = Depends(get_tiktok_service)):
    return tiktok_service.post_clip('teste', r'C:\Users\davib\Downloads\8b1661de-7759-464c-9dfb-df9aa9041a81.mp4')
