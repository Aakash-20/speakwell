from typing import Optional
from pydantic import BaseModel


class CreateBlog(BaseModel):
    title: str
    content: Optional[str] = ""
    slug: Optional[str] = ""

    def __init__(self, **data):
        super().__init__(**data)
        if self.title and not self.slug:
            self.slug = self.title.replace(" ", "-").lower()

