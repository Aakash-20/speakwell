from pydantic import BaseModel
from typing import List

class AddressCreate(BaseModel):
    address: str

class AddressResponse(BaseModel):
    id: int
    address: str

    class Config:
        from_attributes = True

class AddressList(BaseModel):
    addresses: List[AddressResponse]