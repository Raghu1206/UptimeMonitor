from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    url: str

class URLResponse(BaseModel):
    id: int
    url: str
    created_at: datetime

    class Config:
        from_attributes = True

class StatusResponse(BaseModel):
    url: str
    status: str
    status_code: Optional[int]
    response_time: Optional[int]

    class Config:
        from_attributes = True