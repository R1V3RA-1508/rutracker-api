from fastapi import APIRouter, HTTPException, Request
from parser.auth import getSession
from models.errors import NetworkError, NeedCaptcha
from models import LoginQuery
from json import loads

router = APIRouter()


@router.post("/api/login")
async def login(query: LoginQuery, request: Request):
    client = request.app.state.client
    try:
      return await getSession(query=query, client=client)
    except NeedCaptcha as e:
      raise HTTPException(status_code=403, detail=loads(str(e)))
    except NetworkError:
      raise HTTPException(status_code=500, detail="Network error")