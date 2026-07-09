from fastapi import FastAPI 
import httpx
from dotenv import load_dotenv
from os import getenv

from .topics import router as topicRouter

load_dotenv()
BB_SESSION = getenv("BB_SESSION")

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.client = httpx.AsyncClient(
        follow_redirects=True,
        cookies={"bb_session": BB_SESSION},
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.client.aclose()


@app.get("/api/health")
async def health():
    return {"status": "ok"}

app.include_router(topicRouter)