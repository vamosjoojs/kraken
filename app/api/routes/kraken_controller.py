from fastapi import APIRouter, Depends
from typing import List
from app.api.dependencies.kraken import get_kraken_service
from app.models.schemas.kraken import PostQueue
from app.services.kraken_services import KrakenServices

router = APIRouter()


@router.get(
    "/get_posts_queue",
    name="Kraken: Get posts queue",
    status_code=200,
    response_model=List[PostQueue]
)
async def get_posts_queue(kraken_service: KrakenServices = Depends(get_kraken_service)):
    queue_posts = await kraken_service.get_posts_queue_async()
    return queue_posts
