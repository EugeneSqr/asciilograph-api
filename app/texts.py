from fastapi import APIRouter


router = APIRouter()

@router.get("/texts")
async def read_texts():
    return {"Hello": "World"}
