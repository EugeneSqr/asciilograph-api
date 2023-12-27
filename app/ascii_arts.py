from typing import Dict

from fastapi import APIRouter, Depends

from settings import Settings, get_settings
from remote import image_to_ascii_art


router = APIRouter()

@router.get("/ascii_arts")
async def get_ascii_arts(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    return {"Hello": await image_to_ascii_art()}
