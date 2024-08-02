from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CreateBlog(BaseModel):
    title: str
    content: Optional[str] = ""
    slug: Optional[str] = ""

    def __init__(self, **data):
        super().__init__(**data)
        if self.title and not self.slug:
            self.slug = self.title.replace(" ", "-").lower()


class UpdateBlog(CreateBlog):
    pass


class ShowBlog(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    image: str | None

    class Config:
        from_attributes = True
