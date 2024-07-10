from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)

class ShowUser(BaseModel): #user defined rewsponse model, we are not getting the value of hash password
    id : int # it becomes easier for the frontend developers
    email : EmailStr
    is_active : bool

    class Config():
        from_attributes = True