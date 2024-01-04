from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

from queues import process_image
from fileserver import store_image


router = APIRouter()

@router.post("/ascii_arts", response_class=PlainTextResponse)
async def create_ascii_art(request: Request) -> str:
    return await process_image(await store_image(request.stream()))
