from fastapi import FastAPI, HTTPException
import httpx
from parser.topics import getTopic
from models import Topic, NetworkError, NotExistsError
from dotenv import load_dotenv
from os import getenv

load_dotenv()
BB_SESSION = getenv("BB_SESSION")

app = FastAPI()

@app.on_event("startup")
async def startup():
    global client
    client = httpx.AsyncClient(
        follow_redirects=True,
        cookies={"bb_session": BB_SESSION},
    )

@app.on_event("shutdown")
async def shutdown():
    await client.aclose()


@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get('/api/getTopic')
async def get_topic(pageId: int) -> Topic:
    try:
        return await getTopic(pageId, client=client)
    except NotExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NetworkError as e:
        raise HTTPException(status_code=502, detail=str(e))