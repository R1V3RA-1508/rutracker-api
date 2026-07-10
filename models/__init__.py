from pydantic import BaseModel
from typing import Optional

# Topics

class Topic(BaseModel):
    title: str
    body: str
    id: int

# Auth

class LoginQuery(BaseModel):
    username: str
    password: str
    capValue: Optional[str] = None
    capSid: Optional[str] = None
    capField: Optional[str] = None
    redirect: Optional[str] = None

class Session(BaseModel):
    bb_session: str