from datetime import datetime

from fastapi.openapi.models import EmailStr
from pydantic import BaseModel
from typing import Literal


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False


class PostCreate(PostBase):
    pass

## response model

class Post(PostBase):
    id : int
    created_at : datetime
    user_id  : int
    owner : UserOut
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes : int
    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id : int
    dir : bool

