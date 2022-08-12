from fastapi import APIRouter

from app.api.routes import kraken_controller, twitch_controller,\
    twitter_controller, auth_controller, parameters_controller, instagram_controller, youtube_controller

router = APIRouter()

router.include_router(auth_controller.router, tags=['auth'], prefix="/auth")
router.include_router(kraken_controller.router, tags=["kraken"], prefix="/kraken")
router.include_router(twitch_controller.router, tags=["twitch"], prefix="/twitch")
router.include_router(twitter_controller.router, tags=["twitter"], prefix="/twitter")
router.include_router(parameters_controller.router, tags=["parameter"], prefix="/parameter")
router.include_router(instagram_controller.router, tags=["instagram"], prefix="/instagram")
router.include_router(youtube_controller.router, tags=["youtube"], prefix="/youtube")
