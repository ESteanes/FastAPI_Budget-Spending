from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer,String,ForeignKey
from sqlalchemy.orm import relationship

#database model
class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True,index=True)
    author_id = Column(Integer,ForeignKey('users.id'))
    author = relationship("User",back_populates="blogs")
    title = Column(String)
    body = Column(String)
    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship('Blog', back_populates='author')