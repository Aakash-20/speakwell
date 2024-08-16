from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class ShowUser(BaseModel): 
    id : int 
    email : EmailStr

    class Config():
        from_attributes = True