from fastapi import APIRouter, HTTPException, Request
from parser.topics import getTopic
from models import Topic
from models.errors import NetworkError, NotExistsError

router = APIRouter()

@router.get("/api/getTopic")
async def get_topic(pageId: int, request: Request) -> Topic:
    client = request.app.state.client
    try:
        return await getTopic(pageId, client=client)
    except NotExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NetworkError as e:
        raise HTTPException(status_code=502, detail=str(e))