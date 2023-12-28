from typing import Dict

from fastapi import APIRouter

from queues import process_image


router = APIRouter()

@router.get("/ascii_arts")
async def get_ascii_arts() -> Dict[str, str]:
    return {"Hello": await _image_to_ascii_art()}

async def _image_to_ascii_art() -> str:
    image_key = await _store_image()
    return await process_image(image_key)

async def _store_image() -> str:
    return "image key"
