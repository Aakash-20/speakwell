from pydantic import BaseModel


class URLUpdate(BaseModel):
    url: str

    class Config:
        from_attributes = True