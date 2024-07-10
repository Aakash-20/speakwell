from pydantic import BaseModel
from datetime import datetime

class CreateEnquiry(BaseModel):
    course: str
    customer_name: str
    customer_phone: int
    text: str

class ShowEnquiry(BaseModel):
    id: int
    course: str
    customer_name: str
    customer_phone: int
    text: str
    created_at: datetime


    class Config:
        orm_mode = True
