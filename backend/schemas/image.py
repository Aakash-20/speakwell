from pydantic import BaseModel
from datetime import datetime
from typing import List

class ImageUploadResponse(BaseModel):
    filename: str
    url: str

class ImageResponse(BaseModel):
    id: int
    filename: str
    url: str
    created_at: datetime

class ImageListResponse(BaseModel):
    images: List[ImageResponse]
