## Youtube App

Tech Used: Python, FastAPI and SQLite

### Steps to Run

#### Locally Run via virtualenv

- `cd youtube`
- Create Python Virtual Env 
```
python3 -m venv env
source env/bin/activate
```
- Install requirements.txt using `pip -r requirements.txt`
- Run server by `python main.py`

#### Using Dockerfile 

- `docker build -t youtube_app .`
- Update .env file (Based on your choice)
    - TRENDING_TOPIC => Used to fetch topic related recent videos 
    - API_INTERVAL_CALL_IN_SECONDS => Waiting time for fetching recent videos
    - YOUTUBE_API_KEY
- `docker run  -p 8005:8005 -v {Absolute_Project_Path}/storage:/code/storage --env-file ./.env youtube_app`

#### API doc
- - Go to Swagger Doc at http://0.0.0.0:8005/docs#

#### Implemented Bonus Features (Apart from Basic Requirements)

- Optimize search api
