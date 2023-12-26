from typing import Dict

from fastapi import APIRouter, Depends

from settings import Settings, get_settings


router = APIRouter()

@router.get("/ascii_arts")
async def get_ascii_arts(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    return {"Hello": "World"}
