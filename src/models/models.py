from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON

from src.db.database import Base

class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    publish_time = Column(DateTime)
    thumbnails = Column(JSON)
    channel_title = Column(String)
