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
            follow_redirects=False,
            # cookies={"bb_session": BB_SESSION},
            cookies={
                "bb_guid": "t7uf5llJ7XOG",
                "bb_ssl": "1",
                #"cf_clearance": "zknh1qM4.WF6iy28dRHJ6n6N0rL_HvP0kCQNiaqfbC8-1783685786-1.2.1.1-P5qKcMfNH.waRbCHTyGrDMFwCtNw0DsQAf0BWS.aXjhp0_YwfuJzAlHmdGbSxl7bIvLhBWU1tERLaOztJn7aZfKQG8FyiafZjQM5Gfaqmgu8fgFKnVLKiMb51Ch2R60nT8KP7HbQNLFU5eXFjflBuyGgtPbpzTcYq4OiSWn9sRD83i5EJLbaDWPRNwP986Ib_7QMhwd26Lw93EeuGgMupTHJN.uSvxSlIy8ZkvzWnurr461sl15YANljIphm5s9WVZ.g2RTRNzkQPwqUn2TGzBr_hPRseiad6lF_87eWhs0A7aS9BdkP5ZVb8ImAEt7vAstKW6BQS2oSNUCAeG_8qQ",
            },
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                'BB-WebExt': '{"auid":"0kUESMbkLGbz","browser":"firefox-151","proxy":false,"version":"0.9.32"}',
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