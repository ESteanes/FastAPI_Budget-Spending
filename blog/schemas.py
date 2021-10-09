from typing import Optional
from pydantic import BaseModel,Field

#schema for FastAPI
class Blog(BaseModel):
    title: str
    body: str
    author_id: int
        
class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    name: str
    email: str 
    class Config():
        orm_mode = True

class ShowBlog(Blog):
    title: str
    body: str
    author: ShowUser
    class Config():
        orm_mode = True