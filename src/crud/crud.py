from operator import or_
from turtle import title
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import iso8601
from src.models import models
from sqlalchemy.sql import text


from uvicorn.logging import logging
logger = logging.getLogger("uvicorn.info")

def get_videos_on_query(db: Session, search_query:str):
    
    str1 = ""
    str2 = ""
    for word in search_query.split(" "):
        str1 += "LOWER(description) like "+"'%"+word.lower()+"%'"+" and "
        str2 += "LOWER(title) like "+"'%"+word.lower()+"%'"+" and "
    
    str1 = str1.rstrip(" and")
    str2 = str2.rstrip(" and")

    statment = f'select * from videos where {str1} or {str2}'
    logger.info(statment)
    return db.execute(statement=statment).all()
      
def get_videos(db: Session):
    return db.query(models.Videos).order_by(models.Videos.publish_time).all()

def save_videos(db: Session, videos_items:list):
    if len(videos_items) == 0:
        logger.info(f'No new videos found!')    
        return False
    
    for item in videos_items:
        new_video = models.Videos(
            title = item['snippet'].get('title'),
            description = item['snippet'].get('description'),
            publish_time = iso8601.parse_date(item['snippet'].get('publishTime')),
            channel_title = item['snippet'].get('channelTitle'),
            thumbnails = item['snippet'].get('thumbnails')
        )       
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
    logger.info(f'Saved {len(videos_items)} new videos details!')