from datetime import datetime
import json
from typing import List, Optional

from pydantic import BaseModel

class Videos(BaseModel):
    title : str
    description : str
    publish_time : str
    thumbnails : str
    channel_title : str

