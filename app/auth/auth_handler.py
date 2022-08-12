from app.config.config import config
from app.models.schemas.access_token import AccessTokenResponse
from time import time
import jwt


def sign_jwt(
    user_name: str, role="user", seconds_to_expire=config.JWT_SECONDS_TO_EXPIRE
) -> AccessTokenResponse:
    payload = {
        "user_name": user_name,
        "role": role
    }
    if seconds_to_expire > 0:
        payload["exp"] = int(time()) + seconds_to_expire

    token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)

    response = AccessTokenResponse(access_token=token)
    return response


def decode_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, config.JWT_SECRET, [config.JWT_ALGORITHM])
        return decoded
    except:
        return None
