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
