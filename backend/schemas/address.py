from pydantic import BaseModel
from typing import List


class AddressCreate(BaseModel):
    address: str

    class Config:
        from_attributes = True


