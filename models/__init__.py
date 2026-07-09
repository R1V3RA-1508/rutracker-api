from pydantic import BaseModel

# Errors

class NotExistsError(Exception):
    pass

class NetworkError(Exception):
    pass

# Models

class Topic(BaseModel):
    title: str
    body: str
    id: int