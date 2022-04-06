from typing import List

from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitter_service
from app.models.schemas.kraken import CreateTwitterSendMessageTask, GetTwitterSendMessageTask
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


@router.get(
    "/get_send_message_task",
    name="Kraken: Get send message task",
    status_code=200,
    response_model=List[GetTwitterSendMessageTask]
)
async def get_send_message_task(
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return await twitter_service.get_send_message()


@router.put(
    "/edit_send_message_task/{id}",
    name="Kraken: Edit send message task",
    status_code=200,
    response_model=int
)
async def edit_send_message_task(
        id: int,
        edit_twitter_send_message_task: CreateTwitterSendMessageTask,
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return await twitter_service.edit_send_message(id, edit_twitter_send_message_task)


@router.post(
    "/trigger_send_message",
    name="Kraken: Create send message task",
    status_code=201
)
async def trigger_send_message(twitter_service: TwitterServices = Depends(get_twitter_service)):
    return await twitter_service.trigger_send_message_task()
