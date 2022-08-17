from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_reddit_service
from app.auth.auth_bearer import JWTBearer
from app.services.reddit_service import RedditServices


router = APIRouter()


@router.post(
    "/trigger_send_message",
    name="Kraken: Create send message task",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def trigger_send_message(reddit_service: RedditServices = Depends(get_reddit_service)):
    return reddit_service.trigger_send_message()