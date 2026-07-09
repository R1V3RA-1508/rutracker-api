from pydantic import BaseModel

# Errors



# Models

class Topic(BaseModel):
    title: str
    body: str
    id: int