import sys
sys.path.append("../")
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from typing import List
from database import engine, get_db
from schemas import CreatePost, PostOut, ResponseModel
from oauth2 import get_current_user
from typing import Optional

router = APIRouter()

### Retriving all posts
@router.get('/receive',response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),limit: int = 10,skip: int = 0, search: Optional[str]=""):
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True) \
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

### Creating a post using pydantic for schema validation
@router.post('/create',status_code=status.HTTP_201_CREATED,response_model=ResponseModel)
def create_val_post(payload: CreatePost,db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


### Retriving a single post
@router.get('/receive/{id}',response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post


### Deleting a post
@router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    ### Handeling Delete Exception
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} does not exist")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Operation Denied")

    db.query(models.Post).filter(models.Post.id == deleted_post.id).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
     

### Update Post
@router.put('/update/{id}',response_model=ResponseModel)
def update_post(id:int, payload: CreatePost, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    ### Handeling Delete Exception
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Operation Denied")
    
    post_query.update(payload.dict(),synchronize_session=False)
    db.commit()
    # db.query(models.Post).filter(models.Post.id == id).update({"title":})
    # db.commit()

    return post_query.first()
