from typing import Union

from fastapi import FastAPI

from texts import router as texts_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(texts_router)
    return app
