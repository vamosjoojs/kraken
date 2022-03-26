from fastapi import APIRouter

from app.api.routes import kraken_controller, twitch_controller

router = APIRouter()

router.include_router(kraken_controller.router, tags=["kraken"], prefix="/kraken")
router.include_router(twitch_controller.router, tags=["twitch"], prefix="/twitch")
