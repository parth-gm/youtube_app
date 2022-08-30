from fastapi_pagination import response
import requests
from uvicorn.logging import logging

class RequestWrapper:
    def __init__(self,):
        self.logger = logging.getLogger("uvicorn.info")

    def get(self, url:str, query_prams:dict = None):
        try:
            with requests.get(url, query_prams) as data:
                response = data.json()
                if "error" in response:
                    err_msg = response['error'].get('message')
                    self.logger.error(err_msg)
                else:    
                    return response
        except requests.exceptions.ConnectionError as e:
            self.logger.error(
                'Connection Error: Error while connecting to server.')
        except requests.exceptions.Timeout:
            self.logger.error(
                'Connection Timeout: Timeout while connecting to server.')
        except requests.exceptions.TooManyRedirects:
            self.logger.error(
                'TooManyRedirects')
        except requests.exceptions.RequestException as e:
            raise Exception("Unknown Exception")
        return None


