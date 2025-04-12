from fastapi import FastAPI

from app.views import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
def ping() -> None:
    return "pong"
