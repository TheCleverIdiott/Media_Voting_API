from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BIGINT
from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content =Column(String,nullable=False)
    published = Column(Boolean,server_default='True',default=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    phone_number = Column(BIGINT)
    
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))    


class Vote(Base):
    __tablename__ = "votes" 
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)   
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)