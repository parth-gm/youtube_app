from fastapi import APIRouter
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
import asyncio
from src.models import models
from src.crud import crud
from src.utilities.youtube_client import YouTubeClient
from src.db.database import SessionLocal, engine
from fastapi_utils.tasks import repeat_every
from fastapi_pagination import paginate, Params
from uvicorn.logging import logging
import os 

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
    responses={404: {"Error": "Not found"}},
)

logger = logging.getLogger("uvicorn.info")
models.Base.metadata.create_all(bind=engine)
API_INTERVAL_CALL_IN_SECONDS = int(os.environ.get('API_INTERVAL_CALL_IN_SECONDS', 5*60))#called every 5 min
TRENDING_TOPIC = os.environ.get('SEARCH_TOPIC', 'cricket')
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

youtube_service = YouTubeClient(TRENDING_TOPIC, api_interval=API_INTERVAL_CALL_IN_SECONDS)
# logger.info()
@router.on_event('startup')
@repeat_every(seconds=API_INTERVAL_CALL_IN_SECONDS)
async def service_tasks_startup(db: Session = next(get_db())):
    logger.info("Background process starts")
    await asyncio.create_task(youtube_service.get_latest_videos(db=db))
    logger.info("Background process End")

@router.get('/getVideos')
def get_videos(db: Session = Depends(get_db), params: Params = Depends()):
    ans = crud.get_videos(db)
    return paginate(ans, params)
    
@router.get('/basicSearch/{search_query}')
def search_videos(search_query:str, db: Session = Depends(get_db)):
    logger.info(f'Performing search on : {search_query}')
    res = crud.get_videos_on_query(db, search_query)
    return res
