from pydantic import BaseModel
from datetime import datetime


class ImageResponse(BaseModel):
    id: int
    filename: str
    url: str
    created_at: datetime


class ImageListResponse(ImageResponse):
    pass
        
    class Config:
        from_attributes = True
