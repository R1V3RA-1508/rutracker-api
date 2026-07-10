from fastapi import APIRouter, HTTPException, Request
from parser.auth import getSession
from models.errors import NetworkError, NeedCaptcha, InvalidPassError
from models import LoginQuery, Session
from json import loads

router = APIRouter()


@router.post("/api/login")
async def login(query: LoginQuery, request: Request) -> Session:
    client = request.app.state.client
    try:
      return await getSession(query=query, client=client)
    except NeedCaptcha as e:
      raise HTTPException(status_code=403, detail=loads(str(e)))
    except NetworkError:
      raise HTTPException(status_code=500, detail="Network error")
    except InvalidPassError as e:
      raise HTTPException(status_code=403, detail=str(e))