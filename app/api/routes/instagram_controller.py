from typing import List

from fastapi import APIRouter, Depends
from app.api.dependencies.kraken import get_instagram_bot_service
from app.auth.auth_bearer import JWTBearer
from app.models.schemas.kraken import CreateFollowInstagramTask, GetInstagramFollowTask
from app.services.instagram_bot_service import InstagramBotServices

router = APIRouter()


@router.post(
    "/create_follow_task",
    name="Kraken: Create follow task",
    status_code=200,
    response_model=int,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def create_follow_task(
        create_instagram_follow_task: CreateFollowInstagramTask,
        instagram_service: InstagramBotServices = Depends(get_instagram_bot_service)):
    return instagram_service.create_follow_task(create_instagram_follow_task)


@router.get(
    "/get_follow_task",
    name="Kraken: Get follow task",
    status_code=200,
    response_model=List[GetInstagramFollowTask],
    dependencies=[Depends(JWTBearer(role="user"))],
)
async def get_follow_task(
        instagram_service: InstagramBotServices = Depends(get_instagram_bot_service)):
    return instagram_service.get_follow()


@router.post(
    "/trigger_follow",
    name="Kraken: Create follow task",
    status_code=201,
    dependencies=[Depends(JWTBearer(role="user"))],
)
def trigger_follow(instagram_service: InstagramBotServices = Depends(get_instagram_bot_service)):
    return instagram_service.trigger_follow_task()