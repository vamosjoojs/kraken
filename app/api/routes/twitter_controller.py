from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitter_service
from app.models.schemas.kraken import CreateTwitterSendMessageTask
from app.services.twitter_service import TwitterServices

router = APIRouter()


@router.post(
    "/create_send_message_task",
    name="Kraken: Create send message task",
    status_code=200,
    response_model=int
)
async def create_send_message_task(
        create_twitter_send_message_task: CreateTwitterSendMessageTask,
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return await twitter_service.create_send_message(create_twitter_send_message_task)


@router.post(
    "/trigger_send_message",
    name="Kraken: Create send message task",
    status_code=201
)
async def trigger_send_message(twitter_service: TwitterServices = Depends(get_twitter_service)):
    return await twitter_service.trigger_send_message_task()
