from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from .database import  Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, nullable= False, primary_key=True)
    title = Column(String, nullable =False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False )
    created_at =  Column(TIMESTAMP(timezone=True),nullable= False, server_default=text('now()'))
    owner = relationship('User')


    def __str__(self):
        return f"Post(id = {self.id}, title= {self.title}, content = {self.content})"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable= False, primary_key=True)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    created_at =  Column(TIMESTAMP(timezone=True),nullable= False, server_default=text('now()'))

    def __str__(self):
        return f"User(id = {self.id}, email ={self.email}, created_at = {self.created_at})"


class Vote(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)

    def __str__(self):
        return f"Vote(post_id = {self.post_id}, user_id = {self.user_id})"
