from pydantic import BaseModel

class ContactCreate(BaseModel):
    name: str
    phone_no: int
    message: str
    branch: str

class ShowContact(ContactCreate):
    id: int

    class Config:
        from_attributes = True
