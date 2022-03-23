import uvicorn

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware
from typing import Callable

from app.api.routes.api import router as api_router
from app.config.config import config


from app.config.logger import Logger


async def catch_exceptions_middleware(request: Request, call_next: Callable) -> Response:
    try:
        return await call_next(request)
    except Exception as ex:
        logger = Logger.get_logger("internal_server_error")
        logger.exception(ex.args[0])
        result = JSONResponse(
            {
                "error": {
                    "message": ex.args[0],
                    "code": 500,
                }
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return result


def get_application() -> FastAPI:
    application = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

    application.middleware("http")(catch_exceptions_middleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
  
    application.include_router(api_router, prefix=config.API_PREFIX)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
