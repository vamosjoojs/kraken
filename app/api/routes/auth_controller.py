from app.api.dependencies.auth import get_auth_service
from app.models.schemas.access_token import AccessTokenInCreate, AccessTokenResponse
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/create_token",
    response_model=AccessTokenResponse,
    name="Auth: Create token",
    dependencies=[Depends(JWTBearer(role="admin"))],
)
def create(
    token: AccessTokenInCreate, auth_service: AuthService = Depends(get_auth_service)
) -> AccessTokenResponse:
    response = auth_service.create(token)

    return response


@router.get(
    "/login",
    response_model=bool,
    name="Auth: Login with token",
)
def create(
    token: str, auth_service: AuthService = Depends(get_auth_service)
) -> bool:
    response = auth_service.login(token)
    return response
