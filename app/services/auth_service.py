from app.auth.auth_bearer import JWTBearer
from app.models.schemas.access_token import AccessTokenInCreate, AccessTokenResponse
from app.auth.auth_handler import sign_jwt, decode_jwt


class AuthService:
    @staticmethod
    def create(access_token_info: AccessTokenInCreate) -> AccessTokenResponse:
        result = sign_jwt(access_token_info.user_name)
        return result

    @staticmethod
    def login(token) -> bool:
        jwt_bearer = JWTBearer()
        return jwt_bearer.verify_jwt(token)
