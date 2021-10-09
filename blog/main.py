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
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
models.Base.metadata.create_all(engine)

@app.get('/')
def index():
    data = {'data':{
                'name':'Ellington',
                'location':'Sydney'
                }
            }
    return data
@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['blog'])
def about(id: int,db:Session = Depends(get_db)):
    return db.query(models.Blog).filter(models.Blog.id==id).first()

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def about(id:int,request: schemas.Blog,db:Session = Depends(get_db)):
    original_post = db.query(models.Blog).filter(models.Blog.id==id).update(request.dict(),synchronize_session=False)
    db.commit()
    updated_blog = models.Blog(title=request.title,
                           body=request.body)
    if original_post is not None: 
        return f"post updated with {updated_blog}"
    else:
        return "post you want to update doesn't exist"

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
def delete(id:int, db:Session=Depends(get_db)):
    original_blog = db.query(models.Blog).filter(models.Blog.id==id)
    original_blog.delete(synchronize_session=False)

    if original_blog.first() is not None:
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with id={id} does not exist')

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict())    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'data': new_blog}


@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
def retrieve_blogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/user',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser],tags=['user'])
def get_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()

@app.get('/user/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowUser,tags=['user'])
def get_users(id:int,db:Session=Depends(get_db)):
    return db.query(models.User).filter(id==id).first()

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

@app.post('/user',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser,tags=['user'])
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashed_pw = pwd_cxt.hash(request.password)
    new_user = models.User(**request.dict())
    new_user.password = hashed_pw
    # new_user = models.User(name=request.name,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user