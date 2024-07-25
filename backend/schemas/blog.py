from typing import Optional
from pydantic import BaseModel, root_validator
from datetime import date

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
    title: str
    content: Optional[str]
    slug: str
    created_at: date
    image: Optional[str] = ""

    class Config:
        orm_mode = True
