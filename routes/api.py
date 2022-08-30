from fastapi import APIRouter
from src.endpoints import videos

router = APIRouter()
router.include_router(videos.router)