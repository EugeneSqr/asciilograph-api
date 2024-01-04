from typing import Dict

from fastapi import APIRouter, Request

from queues import process_image
from fileserver import store_image


router = APIRouter()

@router.post("/ascii_arts")
async def get_ascii_arts(request: Request) -> Dict[str, str]:
    return {"Hello": await process_image(await store_image(request.stream()))}
