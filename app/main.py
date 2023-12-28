from fastapi import FastAPI

from ascii_arts import router as ascii_arts_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(ascii_arts_router)
    return app
