from app.models.schemas.base import Base


class AccessTokenInCreate(Base):
    user_name: str


class AccessTokenResponse(Base):
    access_token: str
