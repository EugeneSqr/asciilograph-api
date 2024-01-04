import logging
from logging.config import dictConfig
from time import gmtime

from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from ascii_arts import router as ascii_arts_router

def create_app() -> FastAPI:
    _configure_logging()
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)
    app.include_router(ascii_arts_router)
    return app

def _configure_logging() -> None:
    format_string = "[%(levelname)s] [%(asctime)s.%(msecs)03dZ] [%(correlation_id)s] %(message)s"
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 32,
            "default_value": "-",
            },
        },
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": format_string,
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "filters": ["correlation_id"],
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "root": {"handlers": ["default"], "level": "INFO"},
        },
    })
    logging.Formatter.converter = gmtime
