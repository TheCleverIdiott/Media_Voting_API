from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass
      
class UserName(BaseModel):
    email: str

class ResponseModel(PostBase):
    id: int 
    created_at: datetime
    owner_id: int
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: ResponseModel
    votes: int

    class Config:
        orm_mode = True

class Register(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    email:EmailStr
    class Config:
        orm_mode = True    

class Token(BaseModel):
    access_token:str
    token_type: str 

class TokenData(BaseModel):
    id:Optional[str] = None

class Login_details(BaseModel):
    username: str
    password: str    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)