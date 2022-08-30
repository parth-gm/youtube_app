
import os
from datetime import datetime, timedelta
from uvicorn.logging import logging
from src.crud import crud
from src.utilities.requests_wrapper import RequestWrapper

class YouTubeClient:
    
    def __init__(self, query_keyword, maxResults=25, api_interval = 60) -> None:
        self.youtube_api_key = os.environ.get('YOUTUBE_API_KEY')
        self.query = query_keyword
        self.api_url = "https://youtube.googleapis.com/youtube/v3/search"
        self.max_res_per_page = maxResults
        self.before_timestamp = None
        self.after_timestamp = None
        self.api_interval = api_interval
        self.logger = logging.getLogger("uvicorn.info")
        
    def _update_before_after_timestamps(self):
        self.after_timestamp = self.before_timestamp or (datetime.utcnow() - timedelta(0,self.api_interval)).isoformat("T") + "Z"
        self.before_timestamp = datetime.utcnow().isoformat("T") + "Z" 
        
    async def get_latest_videos(self, db):
        self.logger.info("Fetching latest videos...")
        self._update_before_after_timestamps()
        params = {"part":"snippet", 
                    "maxResults":self.max_res_per_page,
                    "q":self.query,
                    "key":self.youtube_api_key,
                    "publishedAfter": self.after_timestamp,
                    "publishedBefore": self.before_timestamp
                    }
        self.logger.info(f'using query params: {params}')
        request_obj = RequestWrapper()
        json_dict = request_obj.get(self.api_url, query_prams=params)
        self._save_videos(db, json_dict)

        while(json_dict and json_dict.get('nextPageToken')):
            params['pageToken'] = json_dict['nextPageToken']
            json_dict = request_obj.get(self.api_url, query_prams=params)
            self._save_videos(db, json_dict)

    def _save_videos(self, db, json_dict):
        if json_dict and ('items' in json_dict):
            crud.save_videos(db, json_dict['items'])


