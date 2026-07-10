from fastapi import FastAPI 
import httpx
from httpx_caching import CachingClient
from dotenv import load_dotenv
from os import getenv
from .auth import router as authRouter
from .topics import router as topicRouter

load_dotenv()
BB_SESSION = getenv("BB_SESSION")

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.client = CachingClient(
        httpx.AsyncClient(
            follow_redirects=True,
            # cookies={"bb_session": BB_SESSION},
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "rutracker.org",
                "Origin": "https://rutracker.org",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            },
        )
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.client.aclose()


@app.get("/api/health")
async def health():
    return {"status": "ok"}

app.include_router(topicRouter)
app.include_router(authRouter)