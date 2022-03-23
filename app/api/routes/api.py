from fastapi import APIRouter

from app.api.routes import kraken_controller

router = APIRouter()
router.include_router(kraken_controller.router, tags=["kraken"], prefix="/twitch")
