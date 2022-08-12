from typing import List

from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_twitter_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.kraken import CreateTwitterSendMessageTask, GetTwitterSendMessageTask, CreateTwitterFollowTask, \
    GetTwitterFollowTask
from app.services.twitter_service import TwitterServices

router = APIRouter()


@router.post(
    "/create_send_message_task",
    name="Kraken: Create send message task",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def create_send_message_task(
        create_twitter_send_message_task: CreateTwitterSendMessageTask,
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.create_send_message(create_twitter_send_message_task)


@router.post(
    "/create_follow_task",
    name="Kraken: Create follow task",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def create_follow_task(
        create_twitter_follow_task: CreateTwitterFollowTask,
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.create_follow(create_twitter_follow_task)


@router.get(
    "/get_send_message_task",
    name="Kraken: Get send message task",
    status_code=200,
    response_model=List[GetTwitterSendMessageTask],
    dependencies=[Depends(JWTBearer(role="user"))],
)
async def get_send_message_task(
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.get_send_message()


@router.get(
    "/get_follow_task",
    name="Kraken: Get follow task",
    status_code=200,
    response_model=List[GetTwitterFollowTask],
    dependencies=[Depends(JWTBearer(role="user"))],
)
async def get_follow_task(
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.get_follow()


@router.put(
    "/edit_send_message_task/{id}",
    name="Kraken: Edit send message task",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def edit_send_message_task(
        id: int,
        edit_twitter_send_message_task: CreateTwitterSendMessageTask,
        twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.edit_send_message(id, edit_twitter_send_message_task)


@router.post(
    "/trigger_send_message",
    name="Kraken: Create send message task",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def trigger_send_message(twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.trigger_send_message_task()


@router.post(
    "/trigger_follow",
    name="Kraken: Create follow task",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def trigger_follow(twitter_service: TwitterServices = Depends(get_twitter_service)):
    return twitter_service.trigger_follow_task()

