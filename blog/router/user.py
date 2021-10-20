from fastapi import APIRouter,Depends,status,Response
from typing import List
from os import stat
from typing import  List
from fastapi.param_functions import Body
from blog import schemas,models
from passlib.context import CryptContext
from blog import database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=['user']
)



@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def get_users(db:Session=Depends(database.get_db)):
    return db.query(models.User).all()

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def get_users(id:int,db:Session=Depends(database.get_db)):
    return db.query(models.User).filter(id==id).first()

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(database.get_db)):
    hashed_pw = pwd_cxt.hash(request.password)
    new_user = models.User(**request.dict())
    new_user.password = hashed_pw
    # new_user = models.User(name=request.name,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user