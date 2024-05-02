from fastapi import FastAPI
from uvicorn import run
from src.route import profile_route
from src.route import webhook
from src.settings import Env

app = FastAPI()
app.include_router(profile_route.profile_router)
app.include_router(webhook.webhook_router)

Env.main_set_env()

@app.get('/')
async def index():
    return('Welcome to this FastAPI test!')

if __name__ == "__main__":
    run('main:app', host=Env.HOST, port=Env.PORT, reload=Env.RELOAD)
