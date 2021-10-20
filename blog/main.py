from os import stat
from fastapi import FastAPI,Depends,status,Response
from typing import Optional, List
from fastapi.exceptions import HTTPException

from fastapi.param_functions import Body
from sqlalchemy.sql.expression import false, update
from sqlalchemy.sql.functions import user
from starlette.status import HTTP_202_ACCEPTED
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session,relationship
import json
from passlib.context import CryptContext
from blog.router import blog,user

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)


        
models.Base.metadata.create_all(engine)

@app.get('/')
def index():
    data = {'data':{
                'name':'Ellington',
                'location':'Sydney'
                }
            }
    return data

