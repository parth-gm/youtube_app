## Youtube App

Tech Used: Python, FastAPI and SQLite

### Steps to Run

#### Local

- `cd youtube`
- Create Python Virtual Env 
```
python3 -m venv env
source env/bin/activate
```
- Install requirements.txt using `pip -r requirements.txt`
- Run server by `python main.py`
- Go to Swagger Doc at http://127.0.0.1:8000/docs#/


### Using Dockerfile 

- `docker build -t youtube_app .`
- Update .env file (Based on your choice)
    - TRENDING_TOPIC
    - API_INTERVAL_CALL_IN_SECONDS
    - YOUTUBE_API_KEY
- `docker run  -p 8005:8005 -v {Project_Path}/storage:/code/storage --env-file ./.env youtube_app`

## Implemented Bonus Features (Apart from Basic Requirements)

- Optimize search api