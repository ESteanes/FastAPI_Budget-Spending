from fastapi import APIRouter,Depends,status,Response
from typing import List
from os import stat
from typing import  List
from fastapi.exceptions import HTTPException
from blog import schemas,models
from sqlalchemy.orm import Session
from blog import database


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

#comment


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def about(id: int,db:Session = Depends(database.get_db)):
    return db.query(models.Blog).filter(models.Blog.id==id).first()

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def about(id:int,request: schemas.Blog,db:Session = Depends(database.get_db)):
    original_post = db.query(models.Blog).filter(models.Blog.id==id).update(request.dict(),synchronize_session=False)
    db.commit()
    updated_blog = models.Blog(title=request.title,
                           body=request.body)
    if original_post is not None: 
        return f"post updated with {updated_blog}"
    else:
        return "post you want to update doesn't exist"

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db:Session=Depends(database.get_db)):
    original_blog = db.query(models.Blog).filter(models.Blog.id==id)
    original_blog.delete(synchronize_session=False)

    if original_blog.first() is not None:
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with id={id} does not exist')

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(**request.dict())    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'data': new_blog}


@router.get('/',response_model=List[schemas.ShowBlog])
def retrieve_blogs(db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs