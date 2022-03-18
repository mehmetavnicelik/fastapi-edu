from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint



class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserServiceResponse(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostServiceResponse(PostBase): ##Post in original
    id: int
    created_at: datetime
    owner_id: int
    owner: UserServiceResponse
 
    class Config:
        orm_mode=True

class PostServiceResponse4Vote(PostBase): ##I dont know why but this doesnt work in "joins" case
    Post:PostServiceResponse
    votes:int
    class Config:
        orm_mode:True


class Token(BaseModel):
    access_token: str 
    token_type: str

    class Config:
        orm_mode=True

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #lessthan or equal to1